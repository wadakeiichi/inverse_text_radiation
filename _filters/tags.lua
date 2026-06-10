-- tags.lua
-- 本文中の "[tag:形]" "[tag:線]" などを <span class="tag">[形]</span> に変換する。

function Str(el)
  local tag = el.text:match("%[tag:([^%]]+)%]")
  if tag then
    return pandoc.RawInline("html", '<span class="tag">[' .. tag .. ']</span>')
  end
  return el
end
