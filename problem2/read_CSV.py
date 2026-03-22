def read_and_print_csv(file_path):
    try:
        file_obj = open(file_path, 'r', encoding='utf-8')
        try:
            content = file_obj.read()
            print(content)
        finally:
            file_obj.close()
    except FileNotFoundError:
        print('지정된 파일을 찾을 수 없습니다.')
    except PermissionError:
        print('파일을 읽을 권한이 없습니다.')
    except Exception as e:
        print('알 수 없는 오류가 발생했습니다: ' + str(e))

if __name__ == '__main__':
    csv_file_name = 'Mars_Base_Inventory_List.csv'
    read_and_print_csv(csv_file_name)