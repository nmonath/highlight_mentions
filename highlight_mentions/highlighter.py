
from absl import logging
from typing import Iterable, Callable
from faker import Factory

logging.info(logging.DEBUG)

class Doc(object):
    def __init__(self, name, text, mentions):
        self.name = name
        self.text = text
        self.mentions = mentions


class Mention(object):
    def __init__(self, start_char_offset, end_char_offset, text_span, entity_id):
        self.start_char_offset = start_char_offset
        self.end_char_offset = end_char_offset
        self.text_span = text_span
        self.entity_id = entity_id


def highlight_texts(text: str, list_of_mentions: Iterable[Mention], get_color: Callable[[Mention], str]) -> str:
    """Produce HTML that labels the entities in the given span. """

    def get_mention_base(color):
        return """
                <mark class="entity" style="background: {bg}; padding: 0.15em 0.15em; margin: 0 0.25em; line-height: 1.5; border-radius: 0.15em">
                    {text}
                    <span style="font-size: 0.8em; font-weight: bold; line-height: 1.5; border-radius: 0.15em; text-transform: uppercase; vertical-align: middle; margin-right: 0.15rem">{label}</span>
                </mark>
                """.replace("{bg}", color)

    def get_mention_string(text, color, label):
        return get_mention_base(color).replace("{text}", text).replace("{label}", label)

    mentions = [[m.start_char_offset, m.end_char_offset, m.entity_id, m.end_char_offset-m.start_char_offset, m] for m in list_of_mentions]
    mentions = sorted(mentions, key=lambda x: (x[1], -x[0]))
    while mentions:
        last_m = mentions[-1]
        outer_most_containing = [m for m in mentions[:-1] if last_m[1]>= m[0]]
        if outer_most_containing:
            outer_most_containing = max(outer_most_containing, key=lambda x: x[1])
        else:
            outer_most_containing = None
        logging.debug('last_m %s', str(last_m))
        logging.debug('outer_most_containing %s', str(outer_most_containing))
        # if e is candidate and is not overlapping
        if outer_most_containing is None or last_m[0] > outer_most_containing[1]:
            logging.debug('case 1: adding %s', str(last_m))
            s, e, t, span_len, m = last_m
            color = get_color(m)
            rs = get_mention_string(text[s:e], color, t)
            text = text[:s] + rs + text[e:]
            logging.debug('len(rs)%s', len(rs))
            mentions.pop()
        elif outer_most_containing is None or last_m[1] > outer_most_containing[0]:
            logging.debug('case 2: adding %s', str(last_m))
            s, e, t, span_len, m = last_m
            color = get_color(m)
            rs = get_mention_string(text[s:e], color, t)
            text = text[:s] + rs + text[e:]
            logging.debug('len(rs)%s', len(rs))
            mentions.pop()
            outer_most_containing[1] += len(rs) - (e -s)
        else:
            logging.debug('case 3: adding %s', str(outer_most_containing))
            s, e, t, span_len, m = outer_most_containing
            color = get_color(m)
            rs = get_mention_string(text[s:e], color, t)
            text = text[:s] + rs + text[e:]
            mentions.pop()
            mentions.pop()
            mentions.insert(last_m, 0)
    while mentions:
        s, e, t, link = mentions.pop()
        color = get_color(t)
        rs = get_mention_string(text[s:e], color, t)
        text = text[:s] + rs + text[e:]
    return text


class Highlighter(object):

    def __init__(self):
        self.colors = dict()
        self.color_maker = Factory.create()

    def head(self):
        head = """
            <head>
            <!--Import Google Icon Font-->
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            
            <!--Import materialize.css-->
            <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
            
            <!--Let browser know website is optimized for mobile-->
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            
            <link rel="icon" type="image/ico" href="./favicon.ico">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
        """
        return head

    def get_color(self, mention: Mention) -> str:
        if mention.entity_id not in self.colors:
            self.colors[mention.entity_id] = self.color_maker.hex_color()
        return self.colors[mention.entity_id]

    def _format_doc(self, doc: Doc):
        """

        :param doc:
        :param chain_to_annotate:
        :return:
        """

        res = """
        <div class="divider"></div>
        <div class="section">
            <h3> %s </h3>
            <div class="row">
                <div class="col s12">
                    %s
                </div>
            </div>
        </div>
        """ % (doc.name, highlight_texts(doc.text, doc.mentions, self.get_color))
        return res

    def html_page(self, doc: Doc):
        res = """
        <!DOCTYPE html>
        <html>
        
        <!-- head -->
        %s
        
        <body>
        <div class="container">
      
        <!-- Contents -->
        %s
        
        </div>
        
        <!-- scripts -->
        %s
        
        </body>
        </html>
        """ % (
            self.head(),
            self._format_doc(doc),
            self.scripts()
        )
        return res

    def scripts(self):
        res = """
            <script type="text/javascript" src="js/materialize.min.js"></script>

            <script>
            var elem = document.querySelectorAll('.collapsible.expandable');
            var instance = M.Collapsible.init(elem, {
            accordion: false
            });
            </script>

            <script>
              var elem = document.querySelectorAll('.fixed-action-btn');
              var instance = M.FloatingActionButton.init(elem, {});
            </script>
        """
        return res
