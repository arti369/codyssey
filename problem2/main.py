def process_inventory_with_missing_data(file_path):
    try:
        file_obj = open(file_path, 'r', encoding='utf-8')
        try:
            content = file_obj.read()
        finally:
            file_obj.close()
            
        lines = content.strip().split('\n')
        
        if not lines:
            print('파일이 비어있습니다.')
            return

        header = lines[0].strip().split(',')
        inventory_list = []
        invalid_data_list = []
        
        for line in lines[1:]:
            line = line.strip()
            if line:
                row = line.split(',')
                
                # 1. 컬럼 수가 부족한 경우 (데이터 누락) 예외 처리
                if len(row) < 5:
                    invalid_data_list.append(row)
                    continue
                
                flammability_str = row[4].strip()
                
                # 2. 인화성 값이 비어있는 경우 예외 처리
                if not flammability_str:
                    invalid_data_list.append(row)
                    continue
                
                # 3. 숫자로 변환할 수 없는 값이 들어있는 경우 예외 처리
                try:
                    float_val = float(flammability_str)
                    inventory_list.append(row)
                except ValueError:
                    invalid_data_list.append(row)
        
        # 정렬 전 원본 데이터 통째로 출력
        print('\n--- 정렬 전 원본 화물 목록 ---')
        print(header)
        print(inventory_list)
                    
        # 정상적인 데이터만 모인 리스트를 인화성 기준으로 내림차순 정렬
        inventory_list.sort(key=lambda x: float(x[4].strip()), reverse=True)
        
        # 정렬 후 데이터 출력
        print('\n--- 인화성이 높은 순으로 정렬된 화물 목록 ---')
        print(header)
        for item in inventory_list:
            print(item)
            
        # 정렬된 전체 데이터를 이진 파일(Binary)로 저장 추가
        try:
            bin_file_path = 'Mars_Base_Inventory_List.bin'
            bin_file_obj = open(bin_file_path, 'wb')
            try:
                # 헤더를 바이트로 변환하여 저장
                header_line = ','.join(header) + '\n'
                bin_file_obj.write(header_line.encode('utf-8'))
                
                # 정렬된 데이터를 순회하며 바이트로 변환하여 저장
                for item in inventory_list:
                    row_line = ','.join(item) + '\n'
                    bin_file_obj.write(row_line.encode('utf-8'))
            finally:
                bin_file_obj.close()
            print('\n안내: 정렬된 화물 목록이 ' + bin_file_path + ' 이진(Binary) 파일로 성공적으로 저장되었습니다.')
        except PermissionError:
            print('\n오류: ' + bin_file_path + ' 파일을 저장할 권한이 없습니다.')
        except Exception as e:
            print('\n오류: 이진 파일 저장 중 알 수 없는 문제가 발생했습니다: ' + str(e))
            
        # 인화성 지수가 0.7 이상인 화물 목록 추출 및 출력 추가
        high_flammability_list = []
        for item in inventory_list:
            if float(item[4].strip()) >= 0.7:
                high_flammability_list.append(item)
                
        print('\n--- 인화성 지수가 0.7 이상인 화물 목록 ---')
        print(header)
        for item in high_flammability_list:
            print(item)
            
        # 추출된 위험 화물 목록을 CSV 파일로 저장
        try:
            danger_file_path = 'Mars_Base_Inventory_danger.csv'
            out_file_obj = open(danger_file_path, 'w', encoding='utf-8')
            try:
                # 헤더 문자열을 만들어 저장 (리스트 요소들을 쉼표로 연결하고 끝에 줄바꿈 추가)
                header_line = ','.join(header) + '\n'
                out_file_obj.write(header_line)
                
                # 데이터 리스트를 순회하며 각각의 행을 문자열로 만들어 저장
                for item in high_flammability_list:
                    row_line = ','.join(item) + '\n'
                    out_file_obj.write(row_line)
            finally:
                out_file_obj.close()
            print('\n안내: 인화성 0.7 이상인 위험 화물 목록이 ' + danger_file_path + ' 파일로 성공적으로 저장되었습니다.')
        except PermissionError:
            print('\n오류: ' + danger_file_path + ' 파일을 저장할 권한이 없습니다.')
        except Exception as e:
            print('\n오류: 파일 저장 중 알 수 없는 문제가 발생했습니다: ' + str(e))

        # 잘못된 형식의 데이터 리스트 출력 추가
        print('\n--- 잘못된 형식의 데이터 목록 ---')
        print(invalid_data_list)
            
    except FileNotFoundError:
        print('지정된 파일을 찾을 수 없습니다.')
    except PermissionError:
        print('파일을 읽을 권한이 없습니다.')
    except Exception as e:
        print('알 수 없는 오류가 발생했습니다: ' + str(e))

if __name__ == '__main__':
    csv_file_name = 'Mars_Base_Inventory_List.csv'
    process_inventory_with_missing_data(csv_file_name)