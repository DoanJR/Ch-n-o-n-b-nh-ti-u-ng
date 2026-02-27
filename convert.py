from docling.document_converter import DocumentConverter

PDF_PATH = "Báo cáo Bài tập lớn IT3160 - Nhóm 7.pdf"
OUTPUT_MD = "bc.md"

converter = DocumentConverter()
result = converter.convert(PDF_PATH)
doc = result.document

print("\n=== DOC INFO ===")
print("Document:", doc.name)
print("Total pages:", doc.num_pages())
print("================\n")

pages = {}

for item, stack in doc.iterate_items():
    # DEBUG: In ra loại và nội dung item, stack
    print(f"item type: {type(item)}, item: {repr(item)}")
    print(f"stack type: {type(stack)}, stack: {repr(stack)}")
    # chỉ lấy text
    if not hasattr(item, "text") or not item.text:
        continue

    page_no = None
    found_in_stack = False

    # chỉ lặp nếu stack là list hoặc tuple
    if isinstance(stack, (list, tuple)):
        for idx, s in enumerate(stack):
            print(f"  stack[{idx}] type: {type(s)}, attrs: {dir(s)}")
            if hasattr(s, "page_no"):
                print(f"    stack[{idx}].page_no: {getattr(s, 'page_no', None)}")
                page_no = s.page_no
                found_in_stack = True
                break
    # nếu stack là object có page_no
    elif hasattr(stack, "page_no"):
        print(f"  stack.page_no: {getattr(stack, 'page_no', None)}")
        page_no = stack.page_no
        found_in_stack = True

    # Nếu không tìm thấy page_no trong stack, thử lấy từ item
    if page_no is None and hasattr(item, "page_no"):
        print(f"  item.page_no: {getattr(item, 'page_no', None)}")
        page_no = item.page_no

    # Nếu vẫn không có, thử lấy từ item.prov[0].page_no
    if page_no is None and hasattr(item, "prov"):
        prov = getattr(item, "prov", None)
        if isinstance(prov, list) and len(prov) > 0:
            first_prov = prov[0]
            if hasattr(first_prov, "page_no"):
                print(f"  item.prov[0].page_no: {getattr(first_prov, 'page_no', None)}")
                page_no = first_prov.page_no

    if page_no is None:
        print("  [WARNING] Không tìm thấy page_no cho item này!\n")
        print("    item attributes:")
        for attr in dir(item):
            if not attr.startswith('__'):
                try:
                    print(f"      {attr}: {getattr(item, attr)}")
                except Exception as e:
                    print(f"      {attr}: <error: {e}>")
        if isinstance(stack, (list, tuple)):
            for idx, s in enumerate(stack):
                print(f"    stack[{idx}] attributes:")
                for attr in dir(s):
                    if not attr.startswith('__'):
                        try:
                            print(f"      {attr}: {getattr(s, attr)}")
                        except Exception as e:
                            print(f"      {attr}: <error: {e}>")
        else:
            print(f"    stack attributes:")
            for attr in dir(stack):
                if not attr.startswith('__'):
                    try:
                        print(f"      {attr}: {getattr(stack, attr)}")
                    except Exception as e:
                        print(f"      {attr}: <error: {e}>")
        print()
        continue

    pages.setdefault(page_no, []).append(item.text.strip())

print("Collected pages:", sorted(pages.keys()))

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    for page_no in sorted(pages.keys()):
        f.write(f"\n\n<!-- Page {page_no} -->\n\n")
        for line in pages[page_no]:
            f.write(line + "\n")

print("\n DONE")
print("Pages written:", len(pages))
print("Output:", OUTPUT_MD)
