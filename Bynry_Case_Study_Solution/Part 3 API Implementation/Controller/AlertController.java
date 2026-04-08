package Part 3 API Implementation.Controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/companies")
public class AlertController {

    private final AlertService alertService;

    public AlertController(AlertService alertService) {
        this.alertService = alertService;
    }

    @GetMapping("/{companyId}/alerts/low-stock")
    public ResponseEntity<LowStockAlertResponse> getLowStockAlerts(
            @PathVariable Long companyId,
            // Pagination is crucial for scalability, defaulting to first 100
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "100") int size) {
        
        LowStockAlertResponse response = alertService.getLowStockAlerts(companyId, page, size);
        return ResponseEntity.ok(response);
    }
}
