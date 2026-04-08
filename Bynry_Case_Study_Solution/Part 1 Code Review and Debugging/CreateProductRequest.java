import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import java.math.BigDecimal;

public class CreateProductRequest {
    
  @NotBlank
  private String name;

  @NotBlank
  private String sku;

  @NotNull
  @PositiveOrZero
  private BigDecimal price;

  @NotNull
  private Long warehouseId;

  @NotNull
  @PositiveOrZero
  private Integer initialQuantity;

  private String description;

  public String getName() {
    return name; 
  }

  public void setName(String name) {
    this.name = name; 
  }
  
  public String getSku() { 
    return sku; 
  }

  public void setSku(String sku) { 
    this.sku = sku; 
  }
  
  public BigDecimal getPrice() {
    return price; 
  }

  public void setPrice(BigDecimal price) { 
    this.price = price; 
  }
  
  public Long getWarehouseId() { 
    return warehouseId; 
  }

  public void setWarehouseId(Long warehouseId) { 
    this.warehouseId = warehouseId; 
  }
  
  public Integer getInitialQuantity() { 
    return initialQuantity; 
  }

  public void setInitialQuantity(Integer initialQuantity) { 
    this.initialQuantity = initialQuantity; 
  }
  
  public String getDescription() { 
    return description; 
  }
  
  public void setDescription(String description) { 
    this.description = description; 
  }

}