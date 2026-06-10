-- boxed-factor.lua
-- 数式中に \boxed{...} が現れたとき、特別なクラスを付与して
-- CSS で見た目を統一する補助 filter。
-- KaTeX/MathJax は \boxed をネイティブにサポートするので、
-- 通常はこの filter はパススルー。
-- 将来 boxed 因子を切り替えやすくするために shortcode を追加。

-- {{< highlight-factor name="hnu" >}} のようなショートコードで
-- 中心地図の特定因子を強調する切替フックを準備（実装は include 側）。

function Shortcode(name, args, kwargs)
  if name == "highlight-factor" then
    local factor_name = kwargs.name or args[1] or "default"
    -- 現状はメタデータをそのまま埋め込む（include 側で利用）
    return pandoc.RawBlock("html",
      '<div class="highlighted-factor" data-factor="' .. factor_name .. '"></div>')
  end
end
