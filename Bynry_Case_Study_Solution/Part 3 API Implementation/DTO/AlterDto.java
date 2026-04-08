public class AlertDto {
    private Long productId;
    private String productName;
    private String sku;
    private Long warehouseId;
    private String warehouseName;
    private Integer currentStock;
    private Integer threshold;
    private Integer daysUntilStockout;
    private SupplierDto supplier;

    // Getters, setters, and constructors omitted for brevity
}