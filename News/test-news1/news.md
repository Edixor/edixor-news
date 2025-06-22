# News test1

# Заголовок H1 — Edixor Markdown Showcase

## Заголовок H2 — Основные элементы

### Заголовок H3 — Форматирование текста

**Жирный текст**  
*Курсивный текст*  
~~Зачёркнутый текст~~  
`Моноширинный текст`  
<ins>Подчёркнутый (через HTML)</ins>

> Это цитата. Используется для выделения важных блоков текста.

---

### Заголовок H3 — Списки

- Маркированный список
  - Вложенный пункт
  - Второй уровень
    - Третий уровень

1. Нумерованный список
2. Второй элемент
   1. Вложенный нумерованный
   2. И ещё один

- [x] Завершённый чекбокс
- [ ] Незавершённый чекбокс

---

### Заголовок H3 — Ссылки и изображения

[Ссылка на GitHub](https://github.com/TerafDev/Edixor)  
![Пример изображения](https://via.placeholder.com/300x100.png?text=Preview)

---

### Заголовок H3 — Код

#### Однострочный код

Пример использования `ShowTab<YourTab>()`.

#### Блок кода

```csharp
using UnityEditor;
using UnityEngine;

public class ExampleWindow : EditorWindow
{
    [MenuItem("Window/Example")]
    public static void ShowWindow()
    {
        GetWindow<ExampleWindow>("Example");
    }
}
