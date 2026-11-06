import json
from pkg.book_tools import read_books, write_books, search_books, show_books


def main():
    """主程式進入點，管理書籍系統運作流程。"""
    book_file = "books.json"
    output_file = "output.json"

    try:
        books = read_books(book_file)
    except FileNotFoundError:
        print(f"錯誤：找不到書籍檔案 '{book_file}'，系統終止。")
        return
    except (json.JSONDecodeError, ValueError) as e:
        print(f"錯誤：'{book_file}' 檔案格式損毀或非合法 JSON ({e})，系統終止。")
        return
    except OSError as e:
        print(f"錯誤：讀取檔案時發生系統錯誤 ({e})，系統終止。")
        return

    while True:
        print("\n--- 簡易書籍管理系統 ---")
        print("1. 顯示全部書籍")
        print("2. 新增書籍")
        print("3. 查詢書籍")
        print("4. 變更借閱狀態")
        print("5. 顯示最後 3 筆書籍與統計")
        print("6. 匯出書籍資料")
        print("7. 離開系統")
        print("------------------------")

        choice = input("請選擇功能：").strip()

        if choice == "1":
            print("\n--- 全部書籍 ---")
            show_books(books)

        elif choice == "2":
            while True:
                new_id = input("請輸入書籍編號：").strip()
                if new_id == "":
                    print("書籍編號不可為空，請重新輸入。")
                    continue
                existing_ids = [b["id"] for b in books]
                if new_id in existing_ids:
                    print("書籍編號已存在，請重新輸入。")
                    continue
                break

            while True:
                new_title = input("請輸入書名：").strip()
                if new_title == "":
                    print("書名不可為空，請重新輸入。")
                    continue
                break

            while True:
                new_author = input("請輸入作者：").strip()
                if new_author == "":
                    print("作者不可為空，請重新輸入。")
                    continue
                break

            while True:
                price_str = input("請輸入價格：").strip()
                try:
                    new_price = int(price_str)
                    if new_price <= 0:
                        print("價格須為大於 0 的整數，請重新輸入。")
                        continue
                    break
                except ValueError:
                    print("價格須為大於 0 的整數，請重新輸入。")

            new_book = {
                "id": new_id,
                "title": new_title,
                "author": new_author,
                "price": new_price,
                "borrowed": False,
            }
            books.append(new_book)
            print("新增成功。")

        elif choice == "3":
            while True:
                keyword = input("請輸入書名關鍵字：").strip()
                if keyword == "":
                    print("關鍵字不可為空，請重新輸入。")
                    continue
                break

            matched_books = search_books(books, keyword)
            print("\n--- 查詢結果 ---")
            if matched_books:
                show_books(matched_books)
            else:
                print("查無符合的書籍")

        elif choice == "4":
            target_id = input("請輸入書籍編號：").strip()
            found = False
            for b in books:
                if b["id"] == target_id:
                    b["borrowed"] = not b["borrowed"]
                    new_status = "已借出" if b["borrowed"] else "可借閱"
                    print(f"「{b['title']}」的狀態已變更為：{new_status}")
                    found = True
                    break
            if not found:
                print("查無此書籍編號")

        elif choice == "5":
            if not books:
                print("\n目前沒有書籍資料")
                continue

            last_3_books = books[-3:]
            print("\n--- 最後 3 筆書籍 ---")
            show_books(last_3_books)

            total_count = len(books)
            borrowed_count = len([b for b in books if b["borrowed"]])
            available_count = total_count - borrowed_count
            total_price = sum([b["price"] for b in books])
            avg_price = total_price / total_count

            print("\n--- 書籍統計 ---")
            print(f"書籍總數：{total_count}")
            print(f"可借閱：{available_count}")
            print(f"已借出：{borrowed_count}")
            print(f"價格合計：{total_price:,} 元")
            print(f"平均價格：{avg_price:.2f} 元")

        elif choice == "6":
            try:
                write_books(books, output_file)
                print(f"已匯出 {len(books)} 筆書籍資料至 {output_file}。")
            except OSError as e:
                print(f"匯出失敗，無法寫入檔案：{e}")

        elif choice == "7":
            print("系統已退出。")
            break

        else:
            print("無效的選項，請輸入 1 到 7 之間的數字。")


if __name__ == "__main__":
    main()