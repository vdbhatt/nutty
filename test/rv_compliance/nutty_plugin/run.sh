
test_suite="/workspaces/amaranth_ws/tmp_area/riscv-arch-test/riscv-test-suite/"
test_env="/workspaces/amaranth_ws/tmp_area/riscv-arch-test/riscv-test-suite/env"
work_dir="/workspaces/amaranth_ws/tmp_area/rv_compliance_work_area"
riscof run --config=config.ini --suite=$test_suite --env=$test_env --work-dir=$work_dir --no-browser