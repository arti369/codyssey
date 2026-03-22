import struct

def process_and_save_real_binary(file_path):
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

        # 이진 파일에서는 보통 데이터의 규격이 정해져 있으므로 헤더 문구는 따로 저장하지 않습니다.
        header = lines[0].strip().split(',')
        inventory_list = []
        invalid_data_list = []
        
        for line in lines[1:]:
            line = line.strip()
            if line:
                row = line.split(',')
                
                # 1. 컬럼 수가 부족한 경우 예외 처리
                if len(row) < 5:
                    invalid_data_list.append(row)
                    continue
                
                flammability_str = row[4].strip()
                
                # 2. 인화성 값이 비어있는 경우 예외 처리
                if not flammability_str:
                    invalid_data_list.append(row)
                    continue
                
                # 3. 숫자로 변환할 수 없는 경우 예외 처리
                try:
                    float_val = float(flammability_str)
                    inventory_list.append(row)
                except ValueError:
                    invalid_data_list.append(row)
                    
        # 인화성 기준으로 내림차순 정렬
        inventory_list.sort(key=lambda x: float(x[4].strip()), reverse=True)
        
        # --- struct를 이용한 '진짜 이진 파일' 저장 시작 ---
        try:
            bin_file_path = 'Mars_Base_Inventory_Realbin.bin'
            bin_file_obj = open(bin_file_path, 'wb')
            try:
                # 1. 먼저 전체 데이터의 개수(행 수)를 정수('i', 4바이트)로 압축하여 저장합니다.
                # (나중에 읽을 때 몇 번 반복해서 읽을지 알기 위함입니다.)
                num_rows = len(inventory_list)
                bin_file_obj.write(struct.pack('i', num_rows))
                
                for row in inventory_list:
                    # 2. 앞의 4개 컬럼(물질명, 무게, 비중, 강도)은 문자열이므로 순회하며 저장합니다.
                    for i in range(4):
                        text_bytes = row[i].strip().encode('utf-8')
                        text_len = len(text_bytes)
                        
                        # 문자열의 '길이'를 먼저 4바이트 정수('i')로 압축해 저장
                        bin_file_obj.write(struct.pack('i', text_len))
                        # 그 다음 실제 문자열 바이트를 저장 ('5s', '10s' 같은 형태의 포맷 생성)
                        bin_file_obj.write(struct.pack(str(text_len) + 's', text_bytes))
                    
                    # 3. 5번째 컬럼인 인화성 수치는 실수형('d', 8바이트)으로 완벽하게 압축하여 저장합니다.
                    flammability_val = float(row[4].strip())
                    bin_file_obj.write(struct.pack('d', flammability_val))
                    
            finally:
                bin_file_obj.close()
                
            print('\n--- 정렬 후 화물 목록 (화면 출력용) ---')
            print(header)
            for item in inventory_list:
                print(item)
                
            print('\n안내: struct 모듈을 사용해 진짜 이진 포맷으로 ' + bin_file_path + ' 파일이 성공적으로 저장되었습니다.')
            print('안내: 이제 이 파일은 메모장으로 열면 완전히 깨져서 외계어처럼 보이게 됩니다!')
            
        except PermissionError:
            print('\n오류: ' + bin_file_path + ' 파일을 저장할 권한이 없습니다.')
        except Exception as e:
            print('\n오류: 이진 파일 저장 중 알 수 없는 문제가 발생했습니다: ' + str(e))
            
    except FileNotFoundError:
        print('지정된 파일을 찾을 수 없습니다.')
    except PermissionError:
        print('파일을 읽을 권한이 없습니다.')
    except Exception as e:
        print('알 수 없는 오류가 발생했습니다: ' + str(e))

if __name__ == '__main__':
    csv_file_name = 'Mars_Base_Inventory_List.csv'
    process_and_save_real_binary(csv_file_name)