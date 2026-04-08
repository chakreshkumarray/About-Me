import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/products")
public class ProductController {

private final ProductService productService;

public ProductController(ProductService productService) {
    this.productService = productService;
}

@PostMapping
public ResponseEntity<?> createProduct(@Valid @RequestBody CreateProductRequest request) {
    try {
        Product newProduct = productService.createProductWithInventory(request);
        
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(Map.of(
                    "message", "Product created successfully",
                    "product_id", newProduct.getId()
                ));
                
    } catch (IllegalArgumentException e) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(Map.of("error", e.getMessage()));
                
    } catch (Exception e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "An unexpected error occurred."));
    }
}
}
