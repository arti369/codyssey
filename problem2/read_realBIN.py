import struct

def read_real_binary(file_path):
    try:
        # 이진 파일을 읽기 전용 이진 모드('rb')로 엽니다.
        file_obj = open(file_path, 'rb')
        try:
            # 1. 가장 먼저 저장해둔 전체 데이터의 개수(행 수)를 4바이트 정수('i')로 읽어옵니다.
            num_rows_bytes = file_obj.read(4)
            if not num_rows_bytes:
                print('파일이 비어있거나 읽을 수 없습니다.')
                return
                
            # unpack은 튜플을 반환하므로 [0]을 통해 첫 번째 값을 가져옵니다.
            num_rows = struct.unpack('i', num_rows_bytes)[0]
            inventory_list = []
            
            # 2. 행의 개수만큼 반복하며 데이터를 하나씩 복원합니다.
            for _ in range(num_rows):
                row = []
                
                # 앞의 4개 컬럼(물질명, 무게, 비중, 강도) 복원
                for _ in range(4):
                    # 이번에 읽을 문자열의 '길이'를 먼저 4바이트 정수('i')로 읽어옵니다.
                    text_len_bytes = file_obj.read(4)
                    text_len = struct.unpack('i', text_len_bytes)[0]
                    
                    # 알아낸 길이(text_len)만큼 실제 문자열 바이트를 읽어옵니다.
                    text_bytes = file_obj.read(text_len)
                    
                    # 바이트를 읽어 포맷('...s')에 맞춰 해독한 뒤, 다시 사람이 읽을 수 있는 문자열로 디코딩합니다.
                    unpacked_text = struct.unpack(str(text_len) + 's', text_bytes)[0]
                    text = unpacked_text.decode('utf-8')
                    row.append(text)
                    
                # 3. 5번째 컬럼인 인화성 수치를 8바이트 실수형('d')으로 읽어옵니다.
                flammability_bytes = file_obj.read(8)
                flammability_val = struct.unpack('d', flammability_bytes)[0]
                
                # 리스트에 추가할 때 보기 편하게 문자열로 변환하여 넣습니다.
                row.append(str(flammability_val))
                
                inventory_list.append(row)
                
        finally:
            file_obj.close()
            
        # 복원된 데이터를 화면에 출력합니다.
        print('\n--- 진짜 이진 파일에서 완벽하게 복원된 화물 목록 ---')
        for item in inventory_list:
            print(item)
            
    except FileNotFoundError:
        print('지정된 이진 파일을 찾을 수 없습니다.')
    except PermissionError:
        print('파일을 읽을 권한이 없습니다.')
    except struct.error:
        # struct 모듈이 예상한 바이트 수와 파일 구조가 다를 때 발생하는 오류입니다.
        print('이진 데이터를 해독하는 중 오류가 발생했습니다. 파일 형식이 맞지 않거나 손상되었습니다.')
    except Exception as e:
        print('알 수 없는 오류가 발생했습니다: ' + str(e))

if __name__ == '__main__':
    bin_file_name = 'Mars_Base_Inventory_Realbin.bin'
    read_real_binary(bin_file_name)