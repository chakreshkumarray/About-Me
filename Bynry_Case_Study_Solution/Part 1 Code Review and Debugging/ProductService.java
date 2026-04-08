import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ProductService {
  
  private final ProductRepository productRepository;
  private final InventoryRepository inventoryRepository;

  public ProductService(ProductRepository productRepository, InventoryRepository inventoryRepository) {
      this.productRepository = productRepository;
      this.inventoryRepository = inventoryRepository;
  }

  @Transactional 
  public Product createProductWithInventory(CreateProductRequest request) {
      
      if (productRepository.existsBySku(request.getSku())) {
          throw new IllegalArgumentException("Product with SKU '" + request.getSku() + "' already exists");
      }

      Product product = new Product();
      product.setName(request.getName());
      product.setSku(request.getSku());
      product.setPrice(request.getPrice());
      product.setDescription(request.getDescription());
      
      product = productRepository.save(product);

      Inventory inventory = new Inventory();
      inventory.setProductId(product.getId());
      inventory.setWarehouseId(request.getWarehouseId());
      inventory.setQuantity(request.getInitialQuantity());
      
      inventoryRepository.save(inventory);

      return product;
  }
}
