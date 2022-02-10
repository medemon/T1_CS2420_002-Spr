        for line in lines:
            for employee_info in line:
                f.write(f"{employee_info},")
            f.write('\n')