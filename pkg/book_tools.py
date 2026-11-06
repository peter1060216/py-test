import json


def read_books(file_name: str) -> list:
    """讀取 JSON 書籍資料並回傳。

    Args:
        file_name (str): JSON 檔案路徑

    Returns:
        list: 書籍字典組成的列表
    """
    with open(file_name, "r", encoding="UTF-8") as f:
        data = json.load(f)
    return data


def write_books(books: list, file_name: str) -> None:
    """將書籍資料寫入 JSON 檔案。

    Args:
        books (list): 書籍列表
        file_name (str): 輸出的 JSON 檔案路徑
    """
    with open(file_name, "w", encoding="UTF-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)


def search_books(books: list, keyword: str) -> list:
    """依書名關鍵字查詢書籍並回傳結果。

    Args:
        books (list): 書籍列表
        keyword (str): 查詢關鍵字

    Returns:
        list: 符合條件的書籍列表
    """
    return [b for b in books if keyword.lower() in b["title"].lower()]


def show_books(books: list) -> None:
    """顯示書籍資料。

    Args:
        books (list): 欲顯示的書籍列表
    """
    if not books:
        print("目前沒有書籍資料")
        return

    print(f"{'編號':>4}  {'書籍編號':<8}  {'書名':<16}  {'作者':<8}  {'價格':>8}  {'狀態'}")

    for idx, b in enumerate(books, 1):
        status = "已借出" if b["borrowed"] else "可借閱"
        print(f"{idx:>4}  {b['id']:<8}  {b['title']:<16}  {b['author']:<8}  {b['price']:>8,}  {status}")