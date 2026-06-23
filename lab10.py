import heapq
import time
from collections import Counter


# Узел дерева Хаффмана

class Node:
    __slots__ = ('char', 'freq', 'left', 'right')

    def __init__(self, char, freq, left=None, right=None):
        self.char  = char
        self.freq  = freq
        self.left  = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


# Построение дерева   O(n log n)

def build_huffman_tree(text: str) -> Node:
    freq = Counter(text)
    heap = [Node(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        heapq.heappush(heap, Node(None, lo.freq + hi.freq, lo, hi))

    return heap[0]


# Генерация кодов (обход дерева)  O(n)

def build_codes(node: Node, prefix: str = '', codes: dict = None) -> dict:
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.char is not None:          # лист
        codes[node.char] = prefix or '0'   # единственный символ → '0'
    else:
        build_codes(node.left,  prefix + '0', codes)
        build_codes(node.right, prefix + '1', codes)
    return codes


# Кодирование   O(m)  (m — длина текста)

def encode(text: str, codes: dict) -> str:
    return ''.join(codes[ch] for ch in text)


# Декодирование  O(m)

def decode(encoded: str, root: Node) -> str:
    result = []
    node = root
    for bit in encoded:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            result.append(node.char)
            node = root
    return ''.join(result)


# Вспомогательная печать дерева

def print_tree(node: Node, indent: str = '', last: bool = True):
    connector = '└── ' if last else '├── '
    label = f"'{node.char}' ({node.freq})" if node.char else f"[{node.freq}]"
    print(indent + connector + label)
    children = [c for c in (node.left, node.right) if c]
    for i, child in enumerate(children):
        ext = '    ' if last else '│   '
        print_tree(child, indent + ext, i == len(children) - 1)


# Демонстрация

def main():
    text = input("Введите текст для кодирования: ").strip()
    if not text:
        text = "hello huffman world"
        print(f"Используем текст по умолчанию: «{text}»")

    print("\n" + "=" * 55)
    print("КОД ХАФФМАНА")
    print("=" * 55)

    # Частоты
    freq = Counter(text)
    print(f"\nДлина исходного текста : {len(text)} символов")
    print(f"Уникальных символов    : {len(freq)}")

    # Построение дерева
    t0 = time.perf_counter()
    root = build_huffman_tree(text)
    codes = build_codes(root)
    elapsed_build = time.perf_counter() - t0

    # Словарь кодов
    print("\nСловарь (символ → код Хаффмана):")
    print(f"  {'Символ':<10} {'Частота':<10} {'Код':<20} {'Длина'}")
    for ch in sorted(codes, key=lambda c: freq[c], reverse=True):
        vis = repr(ch) if ch in (' ', '\t', '\n') else ch
        print(f"  {vis:<10} {freq[ch]:<10} {codes[ch]:<20} {len(codes[ch])}")

    # Дерево
    print("\nДерево Хаффмана:")
    print_tree(root)

    # Кодирование
    t0 = time.perf_counter()
    encoded = encode(text, codes)
    elapsed_enc = time.perf_counter() - t0

    orig_bits  = len(text) * 8
    huff_bits  = len(encoded)
    ratio      = huff_bits / orig_bits * 100

    print(f"\nЗакодированная строка ({huff_bits} бит):")
    # Выводим не более 120 символов, чтобы не перегружать экран
    preview = encoded if len(encoded) <= 120 else encoded[:120] + '...'
    print(f"  {preview}")
    print(f"\nСтатистика сжатия:")
    print(f"  Исходный размер : {orig_bits} бит ({len(text)} байт)")
    print(f"  Сжатый размер   : {huff_bits} бит")
    print(f"  Степень сжатия  : {ratio:.1f}%")

    # Декодирование
    t0 = time.perf_counter()
    decoded = decode(encoded, root)
    elapsed_dec = time.perf_counter() - t0

    print(f"\nВосстановленный текст:")
    print(f"  «{decoded}»")
    print(f"  Совпадает с исходным: {decoded == text}")

    # Время
    print(f"\nВремя работы:")
    print(f"  Построение дерева : {elapsed_build:.6f} с")
    print(f"  Кодирование       : {elapsed_enc:.6f} с")
    print(f"  Декодирование     : {elapsed_dec:.6f} с")

    # Сложность
    print(f"\nАнализ сложности (n = кол-во уникальных символов, m = длина текста):")
    print("  Построение дерева : O(n log n)  — n-1 слияний в куче")
    print("  Кодирование       : O(m)        — один проход по тексту")
    print("  Декодирование     : O(m)        — один проход по битам")
    print("  Итого             : O(n log n + m)")


if __name__ == '__main__':
    main()
