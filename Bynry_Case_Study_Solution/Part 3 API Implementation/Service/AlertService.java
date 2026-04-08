package Part 3 API Implementation.Service;

import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class AlertService {

private final InventoryRepository inventoryRepository;
private final SalesRepository salesRepository;

public AlertService(InventoryRepository inventoryRepository, SalesRepository salesRepository) {
  this.inventoryRepository = inventoryRepository;
  this.salesRepository = salesRepository;
}

public LowStockAlertResponse getLowStockAlerts(Long companyId, int page, int size) {
  // 1. Fetch inventory items that are strictly below their product type's threshold
  // Note: In a real app, this should be a single, optimized Native SQL/JPQL query 
  // to prevent pulling thousands of healthy inventory records into server memory.
  List<Inventory> lowStockCandidates = inventoryRepository.findLowStockByCompany(companyId);

  List<AlertDto> generatedAlerts = lowStockCandidates.stream()
      .filter(this::hasRecentSalesActivity) // Business Rule: Must have recent activity
      .map(this::buildAlertDto)
      .collect(Collectors.toList());

  // 2. Wrap in the required response format
  LowStockAlertResponse response = new LowStockAlertResponse();
  response.setAlerts(generatedAlerts);
  response.setTotalAlerts(generatedAlerts.size());

  return response;
}

private boolean hasRecentSalesActivity(Inventory inventory) {
  // Queries DB to check if sum of sales in last 30 days > 0
  return salesRepository.getSalesVolumeLast30Days(inventory.getProductId()) > 0;
}

private AlertDto buildAlertDto(Inventory inv) {
  AlertDto dto = new AlertDto();
  dto.setProductId(inv.getProduct().getId());
  dto.setProductName(inv.getProduct().getName());
  dto.setSku(inv.getProduct().getSku());
  dto.setWarehouseId(inv.getWarehouse().getId());
  dto.setWarehouseName(inv.getWarehouse().getName());
  dto.setCurrentStock(inv.getQuantity());
  dto.setThreshold(inv.getProduct().getType().getLowStockThreshold());

  // Calculate days until stockout safely
  dto.setDaysUntilStockout(calculateDaysUntilStockout(inv));

  // Map supplier if one exists (handling the edge case of no supplier)
  Supplier primarySupplier = inv.getProduct().getPrimarySupplier();
  if (primarySupplier != null) {
      SupplierDto supplierDto = new SupplierDto();
      supplierDto.setId(primarySupplier.getId());
      supplierDto.setName(primarySupplier.getName());
      supplierDto.setContactEmail(primarySupplier.getContactEmail());
      dto.setSupplier(supplierDto);
  }

  return dto;
}

private Integer calculateDaysUntilStockout(Inventory inv) {
  int volumeLast30Days = salesRepository.getSalesVolumeLast30Days(inv.getProductId());
  
  // Edge Case: Prevent Division by Zero if volume is 0 (though our filter should catch this)
  if (volumeLast30Days == 0) return null; 

  double dailyVelocity = (double) volumeLast30Days / 30.0;
  
  // If they are selling less than 1 a day, avoid returning massive numbers
  if (dailyVelocity < 0.1) return 999; 

  return (int) Math.ceil(inv.getQuantity() / dailyVelocity);
}
}
