# DGX Procurement & Setup (Sub-EXP-041A)

## Hardware Procurement Checklist

### DGX Spark Core System
- [ ] **NVIDIA DGX Spark** (~$3,999)
  - 4 TB NVMe M.2 SSD (self-encrypting)
  - 128 GB Unified LPDDR5x RAM
  - Grace Blackwell-class compute
  - Desktop form factor
  - Status: ORDERED (November 2025 delivery)

### Storage Expansion (Target: $800-900 total)
- [ ] **Thunderbolt NVMe RAID Enclosure** (OWC Express 4M2 or equivalent)
  - Thunderbolt 3/4 connectivity
  - 4× M.2 NVMe slots
  - Active cooling
  - macOS/Linux compatible
  - Target cost: $300-350

- [ ] **NVMe SSD Drives** (2× 4TB for initial setup)
  - PCIe Gen4, TLC NAND
  - Target cost: $120-250 each
  - Total capacity: 8 TB usable (RAID 0)

- [ ] **Future Expansion** (2× additional 4TB drives)
  - For 16 TB total capacity
  - Cost: $240-500

### Physical Infrastructure
- [ ] **Power Requirements**
  - Verify outlet capacity (DGX Spark power specs)
  - Consider UPS for stability
  - Check circuit breaker capacity

- [ ] **Cooling & Ventilation**
  - Clear space per NVIDIA guidelines
  - Adequate room temperature
  - Dust-free environment

- [ ] **Desk/Rack Space**
  - DGX Spark footprint: ~18" × 18" × 8"
  - Weight: ~40 lbs
  - Cable management space

### Networking
- [ ] **Primary Connection**
  - Gigabit Ethernet port available
  - Cat6 cable (6-10 ft)
  - Switch/router configuration

- [ ] **Optional High-Speed**
  - 10G/25G Ethernet consideration
  - Thunderbolt networking potential

### Accessories & Cables
- [ ] Power cable (region-specific)
- [ ] Ethernet cable (Cat6)
- [ ] Thunderbolt cable (for storage enclosure)
- [ ] USB-C cable (for initial setup)

## Delivery & Setup Timeline

### Pre-Delivery (Now - November 2025)
- [ ] Confirm delivery address and access
- [ ] Schedule delivery window
- [ ] Arrange for professional installation if needed
- [ ] Prepare physical space and infrastructure

### Delivery Day (November 2025)
- [ ] Unbox and inspect hardware
- [ ] Verify all components present
- [ ] Check for shipping damage
- [ ] Basic power-on test

### Post-Delivery Setup (November 2025)
- [ ] Physical positioning and cable management
- [ ] Initial power and network connection
- [ ] Basic OS installation verification
- [ ] Hardware acceptance testing

## Hardware Validation Tests

### Power-On Self Test
- [ ] System powers on successfully
- [ ] All LEDs illuminate correctly
- [ ] No error beeps or warnings
- [ ] Basic POST completion

### Hardware Diagnostics
- [ ] Memory test (128 GB unified RAM)
- [ ] Storage test (4 TB internal NVMe)
- [ ] Network connectivity test
- [ ] USB/Thunderbolt port functionality

### Performance Baseline
- [ ] CPU/GPU identification
- [ ] Memory bandwidth test
- [ ] Storage I/O performance
- [ ] Network throughput test

## Storage Expansion Setup

### RAID Configuration
- [ ] Install NVMe drives in enclosure
- [ ] Configure RAID 0 for performance
- [ ] Format file system (ext4 or XFS)
- [ ] Mount and verify access

### Performance Validation
- [ ] Sequential read/write speeds (>2000 MB/s)
- [ ] Random I/O performance
- [ ] Sustained load testing
- [ ] Error handling verification

## Integration Testing

### OS Installation
- [ ] Ubuntu LTS compatibility
- [ ] NVIDIA driver installation
- [ ] CUDA toolkit setup
- [ ] Basic GPU acceleration test

### Storage Integration
- [ ] External NVMe mount points
- [ ] File system permissions
- [ ] Backup and recovery procedures
- [ ] Performance under load

## Documentation & Handover

### Setup Documentation
- [ ] Hardware configuration details
- [ ] Cable mapping and connections
- [ ] Performance benchmarks
- [ ] Troubleshooting procedures

### Operational Runbook
- [ ] Power cycling procedures
- [ ] Hardware maintenance schedule
- [ ] Warranty and support information
- [ ] Emergency contact procedures

## Risk Mitigation

### Delivery Delays
- **Impact**: Project timeline slippage
- **Mitigation**: Parallel software development
- **Contingency**: Cloud GPU alternatives for testing

### Hardware Defects
- **Impact**: System unavailability
- **Mitigation**: On-site spares and warranty coverage
- **Contingency**: RMA procedures and loaner systems

### Integration Issues
- **Impact**: Setup delays and compatibility problems
- **Mitigation**: Pre-delivery testing with similar hardware
- **Contingency**: Vendor support and community resources

## Success Criteria

- [ ] All hardware components delivered and operational
- [ ] Physical infrastructure properly configured
- [ ] Hardware validation tests pass
- [ ] Storage expansion integrated and performing
- [ ] Documentation complete and accessible
- [ ] Team trained on basic operations

## Next Steps

1. **Immediate**: Finalize any remaining procurement items
2. **Week 1**: Prepare physical space and infrastructure
3. **Delivery**: Perform hardware validation and setup
4. **Week 1-2**: Complete integration testing
5. **Week 2**: Handover to provisioning team

## Dependencies

- **Vendor**: NVIDIA DGX Spark availability
- **Infrastructure**: Physical space and power requirements
- **Team**: Hardware setup and validation expertise
- **Timeline**: November 2025 delivery window