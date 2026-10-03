# Pull quotes: mark a phrase in a post with <span class="pull">…</span> and it
# stays in the prose as normal text, and is also repeated in large type as an
# <aside class="pullquote"> placed just before its paragraph.
#
# The copy is aria-hidden so screen readers don't read the sentence twice.
# It is added to the final page HTML only, so the RSS feed carries just the
# prose.
class Builders::PullQuotes < SiteBuilder
  def build
    inspect_html do |document|
      document.query_selector_all("article span.pull").each do |span|
        block = span.ancestors("p, li, blockquote").first || span.parent

        aside = document.create_element("aside", class: "pullquote", "aria-hidden": "true")
        aside.inner_html = span.inner_html
        block.add_previous_sibling(aside)
      end
    end
  end
end
