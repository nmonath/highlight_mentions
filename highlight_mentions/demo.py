from absl import logging
from absl import app
from absl import flags
import numpy as np

from highlight_mentions.highlighter import Highlighter, Mention, Doc

def main(argv):

    doc_text = """On the 24th of February, 1815, the look-out at Notre-Dame de la Garde
    signalled the three-master, the _Pharaon_ from Smyrna, Trieste, and
    Naples.
    
    As usual, a pilot put off immediately, and rounding the Château d’If,
    got on board the vessel between Cape Morgiou and Rion island.
    
    Immediately, and according to custom, the ramparts of Fort Saint-Jean
    were covered with spectators; it is always an event at Marseilles for a
    ship to come into port, especially when this ship, like the _Pharaon_,
    has been built, rigged, and laden at the old Phocee docks, and belongs
    to an owner of the city.
    
    The ship drew on and had safely passed the strait, which some volcanic
    shock has made between the Calasareigne and Jaros islands; had doubled
    Pomègue, and approached the harbor under topsails, jib, and spanker,
    but so slowly and sedately that the idlers, with that instinct which is
    the forerunner of evil, asked one another what misfortune could have
    happened on board. However, those experienced in navigation saw plainly
    that if any accident had occurred, it was not to the vessel herself,
    for she bore down with all the evidence of being skilfully handled, the
    anchor a-cockbill, the jib-boom guys already eased off, and standing by
    the side of the pilot, who was steering the _Pharaon_ towards the
    narrow entrance of the inner port, was a young man, who, with activity
    and vigilant eye, watched every motion of the ship, and repeated each
    direction of the pilot.
    
    The vague disquietude which prevailed among the spectators had so much
    affected one of the crowd that he did not await the arrival of the
    vessel in harbor, but jumping into a small skiff, desired to be pulled
    alongside the _Pharaon_, which he reached as she rounded into La
    Réserve basin."""


    m1 = Mention(start_char_offset=doc_text.find('Notre-Dame'),
                 end_char_offset=doc_text.find('Notre-Dame') + len('Notre-Dame'),
                 text_span='Notre-Dame',
                 entity_id='e0')

    m2 = Mention(start_char_offset=doc_text.find('the look-out at Notre-Dame'),
                 end_char_offset=doc_text.find('the look-out at Notre-Dame') + len('the look-out at Notre-Dame'),
                 text_span='the look-out at Notre-Dame',
                 entity_id='e1')

    m3 = Mention(start_char_offset=doc_text.find('Notre-Dame de la Garde'),
             end_char_offset=doc_text.find('Notre-Dame de la Garde') + len(
                 'Notre-Dame de la Garde'),
             text_span='Notre-Dame de la Garder',
             entity_id='e3')

    m4 = Mention(start_char_offset=doc_text.find('Rion island'),
                 end_char_offset=doc_text.find('Rion island') + len(
                     'Rion island'),
                 text_span='Rion island',
                 entity_id='e2')

    m5 = Mention(start_char_offset=doc_text.find('Calasareigne'),
                 end_char_offset=doc_text.find('Calasareigne') + len(
                     'Calasareigne'),
                 text_span='Calasareigne',
                 entity_id='e4')

    doc = Doc('Example Doc', doc_text, [m1, m2, m3, m4, m5])

    highlighter = Highlighter()
    with open('example.html', 'w') as fout:
        fout.write(highlighter.html_page(doc))


if __name__ == "__main__":
    app.run(main)