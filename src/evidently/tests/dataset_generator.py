from evidently.dataset_generators.llm.index import DataCollection

tmpdir = "/tmp/"


def get_content():
    content = """Much that once was is lost, for none now live who remember it.
                It began with the forging of the Great Rings. Three were given to the Elves, immortal, wisest and
                fairest of all beings. Seven to the Dwarf-Lords, great miners and craftsmen of the mountain halls.
                And nine, nine rings were gifted to the race of Men, who above all else desire power. For within these
                rings was bound the strength and the will to govern each race. But they were all of them deceived,
                for another ring was made. Deep in the land of Mordor, in the Fires of Mount Doom, the Dark Lord Sauron
                 forged a master ring, and into this ring he poured his cruelty, his malice and his will to dominate all
                  life.
                One ring to rule them all.
                One by one, the free lands of Middle-Earth fell to the power of the Ring, but there were some who
                 resisted. A last alliance of men and elves marched against the armies of Mordor, and on the very
                 slopes of Mount Doom, they fought for the freedom of Middle-Earth. Victory was near, but the power of
                 the ring could not be undone. It was in this moment, when all hope had faded, that Isildur, son of the
                  king, took up his father’s sword.
                Sauron, enemy of the free peoples of Middle-Earth, was defeated. The Ring passed to Isildur, who had
                this one chance to destroy evil forever, but the hearts of men are easily corrupted. And the ring of
                power has a will of its own. It betrayed Isildur, to his death.
                And some things that should not have been forgotten were lost. History became legend. Legend became
                myth. And for two and a half thousand years, the ring passed out of all knowledge. Until, when chance
                came, it ensnared another bearer.
                It came to the creature Gollum, who took it deep into the tunnels of the Misty Mountains. And there it
                consumed him. The ring gave to Gollum unnatural long life. For five hundred years it poisoned his mind,
                 and in the gloom of Gollum’s cave, it waited. Darkness crept back into the forests of the world.
                 Rumor grew of a shadow in the East, whispers of a nameless fear, and the Ring of Power perceived its
                  time had come. It abandoned Gollum, but then something happened that the Ring did not intend.
                  It was picked up by the most unlikely creature imaginable: a hobbit, Bilbo Baggins, of the Shire.
                For the time will soon come when hobbits will shape the fortunes of all."""
    return content


def test_knowledge_base():
    file_path = tmpdir + "KnowledgeBase.md"
    content = get_content()
    with open(file_path, "w") as f:
        f.write(content)
    knowledge_base = DataCollection.from_files(file_path, chunk_size=50, chunk_overlap=20)
    assert len(knowledge_base.chunks) == 16
    relevant_chunks = knowledge_base.find_relevant_chunks("Who is Sauron?", 3)
    assert len(relevant_chunks) == 3
