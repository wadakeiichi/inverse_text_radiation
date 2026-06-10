-- difficulty-stars.lua
-- 本文中の "[★ 難易度：☆..☆☆☆ ]" や "[difficulty: *...***]" を
-- <span class="difficulty">...</span> に変換する。
-- HTML/PDF/EPUB 共通で機能。

function Str(el)
  -- 「[★ 難易度：☆☆ ]」パターン
  local stars = el.text:match("%[★%s*難易度：([☆]+)%s*%]")
  if stars then
    return pandoc.RawInline("html", '<span class="difficulty">' .. stars .. '</span>')
  end
  return el
end

-- ショートコード形式 {{< difficulty 2 >}} もサポート
function Shortcode(name, args, kwargs)
  if name == "difficulty" then
    local level = tonumber(args[1]) or 2
    local s = string.rep("☆", level)
    return pandoc.RawBlock("html", '<span class="difficulty">' .. s .. '</span>')
  end
end
