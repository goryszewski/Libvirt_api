import subprocess


def f_cmd(domain, execute, args=None):
    execommand = {"execute": execute, "arguments": args}
    print(execommand)

    command = f"virsh qemu-agent-command {domain} {execommand}"

    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

    # Pobranie wyjścia standardowego (stdout)
    output = result.stdout

    # Pobranie kodu błędu (return code) - w przypadku powodzenia będzie 0
    error_code = result.returncode

    return (output,error_code)
