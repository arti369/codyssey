input_filename = 'mission_computer_main.log'
output_filename = 'log_analysis.md'

try:
    with open(input_filename, 'r', encoding='utf-8') as log_file:
        lines = log_file.readlines()

    accident_logs = []
    for line in lines:
        if 'error' in line.lower() or 'warning' in line.lower() or 'unstable' in line.lower() or 'explosion' in line.lower() or 'crashed' in line.lower() or 'powered down' in line.lower() or 'critical' in line.lower():
            accident_logs.append(line.strip())

    report_content = '# 사고 원인 로그 보고서\n\n'
    
    report_content = report_content + '## 1. 개요\n'
    report_content = report_content + '본 보고서는 `mission_computer_main.log` 파일의 로그 데이터를 바탕으로 발생한 사고의 원인 로그를 나타낸 결과입니다.\n\n'
    
    report_content = report_content + '## 2. 이상 징후 및 사고 발생 로그\n'
    report_content = report_content + '```log\n'
    for log in accident_logs:
        report_content = report_content + log + '\n'

    with open(output_filename, 'w', encoding='utf-8') as md_file:
        md_file.write(report_content)

    print('보고서 파일(log_analysis.md)이 성공적으로 생성되었습니다.')

except FileNotFoundError:
    print('오류: 로그 파일을 찾을 수 없습니다.')
except PermissionError:
    print('오류: 파일을 읽거나 쓸 수 있는 권한이 없습니다.')
except Exception as e:
    print(f'파일을 처리하는 중 알 수 없는 오류가 발생했습니다: {e}')