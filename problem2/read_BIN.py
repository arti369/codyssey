def read_and_print_binary(file_path):
    try:
        file_obj = open(file_path, 'rb')
        try:
            binary_content = file_obj.read()
        finally:
            file_obj.close()
            
        decoded_content = binary_content.decode('utf-8')
        
        lines = decoded_content.strip().split('\n')
        
        if not lines:
            print('파일이 비어있습니다.')
            return
        
        header = lines[0].strip().split(',')
        inventory_list = []
        
        for line in lines[1:]:
            line = line.strip()
            if line:
                row = line.split(',')
                inventory_list.append(row)
        
        print(header)
        for item in inventory_list:
            print(item)
        
    except FileNotFoundError:
        print('지정된 이진 파일을 찾을 수 없습니다.')
    except PermissionError:
        print('파일을 읽을 권한이 없습니다.')
    except UnicodeDecodeError:
        print('파일을 디코딩하는 중 오류가 발생했습니다. 올바른 형식의 파일이 아닐 수 있습니다.')
    except Exception as e:
        print('알 수 없는 오류가 발생했습니다: ' + str(e))

if __name__ == '__main__':
    bin_file_name = 'Mars_Base_Inventory_List.bin'
    read_and_print_binary(bin_file_name)