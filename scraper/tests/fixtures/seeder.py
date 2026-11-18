"""Fixture and cache seeder for Books to Scrape pipeline.

Generates realistic HTML fixtures matching the exact DOM structure of Books to Scrape:
- 3 Catalogue pages with pagination (Page 1 -> Page 2 -> Page 3)
- 60 Book detail pages with price, stock, ratings, and descriptions
Enables complete offline testing, unit tests, and instant verification without external network dependence.
"""
from pathlib import Path
from scraper.src.config import CACHE_DIR, FIXTURES_DIR
from scraper.src.client import PoliteClient

BOOKS_DATA = [
    # Page 1 (1-20)
    ("a-light-in-the-attic_1000", "A Light in the Attic", "£51.77", "In stock (22 available)", "Three", "It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition."),
    ("tipping-the-velvet_999", "Tipping the Velvet", "£53.74", "In stock (20 available)", "One", "Nan King, an oyster girl, is captivated by the music hall phenomenon Kitty Butler, a male impersonator extraordinaire treading the boards in Canterbury."),
    ("soumission_998", "Soumission", "£50.10", "In stock (20 available)", "One", "Dans une France assez proche de la notre, un president de la republique issu d'un parti musulman est elu."),
    ("sharp-objects_997", "Sharp Objects", "£47.82", "In stock (20 available)", "Four", "WICKED above her hips, UNCOILED down the outside of her thigh. Fresh from a brief stay at a psych hospital, journalist Camille Preaker faces a troubling assignment."),
    ("sapiens-a-brief-history-of-humankind_996", "Sapiens: A Brief History of Humankind", "£54.23", "In stock (20 available)", "Five", "From a renowned historian comes a groundbreaking narrative of humanity's creation and evolution."),
    ("the-requiem-red_995", "The Requiem Red", "£22.65", "In stock (19 available)", "One", "Patient Twenty-Nine. A monster on the loose inside a high-security psychiatric ward."),
    ("the-dirty-little-secrets-of-getting-your-dream-job_994", "The Dirty Little Secrets of Getting Your Dream Job", "£33.34", "In stock (19 available)", "Four", "Drawing on his experience as a top executive recruiter, Don Georgevich gives job seekers actionable advice."),
    ("the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993", "The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull", "£17.93", "In stock (19 available)", "Three", "A fascinating biographical novel based on the life of Victoria Woodhull, the first woman to run for president."),
    ("the-boys-in-the-boat-nine-americans-and-their-epic-quest-for-gold-at-the-1936-berlin-olympics_992", "The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics", "£22.60", "In stock (19 available)", "Four", "The dramatic story of the American rowing team that stunned the world at the 1936 Berlin Olympics."),
    ("the-black-maria_991", "The Black Maria", "£52.15", "In stock (19 available)", "One", "A devastating and brilliant poetry collection engaging history, grief, and survival."),
    ("starving-hearts-triangular-trade-trilogy-1_990", "Starving Hearts (Triangular Trade Trilogy, #1)", "£13.99", "In stock (19 available)", "Two", "Since her mother died in a freak storm, 16-year-old Abigail's life has been filled with questions."),
    ("shakespeares-sonnets_989", "Shakespeare's Sonnets", "£20.66", "In stock (19 available)", "Four", "This collection of Shakespeare's sonnets includes all 154 poems published in the 1609 Quarto."),
    ("set-me-free_988", "Set Me Free", "£17.46", "In stock (19 available)", "Five", "Bella has lived her whole life in a world of silence, guarded by strict family expectations."),
    ("scott-pilgrims-precious-little-life-scott-pilgrim-1_987", "Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)", "£52.29", "In stock (19 available)", "Five", "Scott Pilgrim's life is totally sweet until Ramona Flowers starts roller-blading through his dreams."),
    ("rip-it-up-and-start-again_986", "Rip it Up and Start Again", "£35.02", "In stock (19 available)", "Five", "Rip It Up and Start Again is the first book-length history of the postpunk era from 1978 to 1984."),
    ("our-band-could-be-your-life-scenes-from-the-american-indie-underground-1981-1991_985", "Our Band Could Be Your Life: Scenes from the American Indie Underground, 1981-1991", "£57.25", "In stock (19 available)", "Three", "This is the never-before-told story of the musical underground that revolutionized American rock."),
    ("olio_984", "Olio", "£23.88", "In stock (19 available)", "One", "Part sonnet, part interview, part history, Olio addresses racial performance in post-Civil War America."),
    ("mesa-selimovic-death-and-the-dervish_983", "Mesa Selimovic: Death and the Dervish", "£56.08", "In stock (19 available)", "Three", "Ahmed Nuruddin is the sheik of a dervish monastery in Sarajevo in the eighteenth century."),
    ("meditations_982", "Meditations", "£25.89", "In stock (19 available)", "Two", "Nearly two thousand years after it was written, Meditations remains profound reading on personal ethics."),
    ("forever-and-forever-the-courtship-of-henry-longfellow-and-fanny-appleton_981", "Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton", "£29.69", "In stock (19 available)", "Three", "A captivating account of the romantic pursuit that inspired some of America's finest poetry."),

    # Page 2 (21-40)
    ("in-her-wake_980", "In Her Wake", "£12.84", "In stock (19 available)", "One", "A devastating psychological drama exploring identity, grief, and stolen lives."),
    ("how-music-works_979", "How Music Works", "£37.32", "In stock (19 available)", "Two", "How Music Works is David Byrne's remarkable celebration of musical form, context, and beauty."),
    ("foolproof-preserving-a-guide-to-small-batch-jams-jellies-pickles-condiments-and-more_978", "Foolproof Preserving: A Guide to Small Batch Jams, Jellies, Pickles, Condiments, and More", "£30.52", "In stock (19 available)", "Three", "Cooking experts share proven methods for homemade preserves that anyone can master."),
    ("chase-me-paris-nights-2_977", "Chase Me (Paris Nights #2)", "£25.27", "In stock (19 available)", "Five", "A passionate romance through the enchanting streets of nighttime Paris."),
    ("black-dust_976", "Black Dust", "£34.53", "In stock (19 available)", "Five", "A grit-infused mystery deep within coal mining territory where secrets are buried deep."),
    ("birdsong-a-story-in-pictures_975", "Birdsong: A Story in Pictures", "£54.64", "In stock (19 available)", "Three", "A lyrical, gorgeously illustrated visual journey celebrating avian diversity."),
    ("americas-war-for-the-greater-middle-east-a-military-history_974", "America's War for the Greater Middle East: A Military History", "£51.22", "In stock (19 available)", "Two", "An essential military history examining three decades of conflict and policy in the Middle East."),
    ("alamo-all-stars-nathan-hales-hazardous-tales-6_973", "Alamo All-Stars (Nathan Hale's Hazardous Tales #6)", "£35.05", "In stock (19 available)", "Three", "A graphic history of the legendary stand at the Alamo, told with wit and precision."),
    ("airframe_972", "Airframe", "£41.83", "In stock (19 available)", "Five", "A fast-paced investigative thriller exploring aviation disaster and corporate cover-ups."),
    ("a-fierce-and-subtle-poison_971", "A Fierce and Subtle Poison", "£28.13", "In stock (19 available)", "Four", "A captivating magical realism novel set in humid, secret-filled San Juan, Puerto Rico."),
    ("a-flight-of-arrows-the-pathfinders-2_970", "A Flight of Arrows (The Pathfinders #2)", "£55.53", "In stock (19 available)", "Five", "The heroic continuation of an epic fantasy quest against formidable ancient foes."),
    ("a-distant-mirror-the-calamitous-14th-century_969", "A Distant Mirror: The Calamitous 14th Century", "£14.58", "In stock (19 available)", "Three", "Barbara Tuchman examines the dramatic, plague-ridden tumult of the 14th century."),
    ("1000-places-to-see-before-you-die_968", "1,000 Places to See Before You Die", "£26.08", "In stock (19 available)", "Five", "The world-famous travel guide inspiring wanderlust with unforgettable destinations."),
    ("13-hours-the-inside-account-of-what-really-happened-in-benghazi_967", "13 Hours: The Inside Account of What Really Happened In Benghazi", "£27.06", "In stock (19 available)", "One", "The harrowing true story of the security operators who defended the US compound in Benghazi."),
    ("the-paris-wife_966", "The Paris Wife", "£15.95", "In stock (18 available)", "Two", "Paula McLain paints an evocative portrait of Ernest Hemingway's marriage in 1920s Paris."),
    ("the-little-paris-bookshop_965", "The Little Paris Bookshop", "£24.73", "In stock (18 available)", "Three", "Monsieur Perdu prescribes books for the hardships of life from his floating barge on the Seine."),
    ("the-guernsey-literary-and-potato-peel-pie-society_964", "The Guernsey Literary and Potato Peel Pie Society", "£49.53", "In stock (18 available)", "One", "An epistolary novel celebrating literature, resilience, and island camaraderie during WWII."),
    ("the-girl-you-left-behind_963", "The Girl You Left Behind", "£15.79", "In stock (18 available)", "One", "Two women separated by a century, connected by a portrait and an enduring fight for love."),
    ("the-forgotten-garden_962", "The Forgotten Garden", "£15.59", "In stock (18 available)", "Four", "A sprawling generational mystery sweeping from Victorian London to coastal Australia."),
    ("the-echo-wife_961", "The Echo Wife", "£27.88", "In stock (18 available)", "Five", "A dark, speculative thriller about cloning, marriage, and moral reckoning."),

    # Page 3 (41-60)
    ("the-book-thief_960", "The Book Thief", "£53.49", "In stock (18 available)", "Five", "Narrated by Death, this bestselling novel tells of young Liesel living in Nazi Germany."),
    ("the-aviators-wife_959", "The Aviator's Wife", "£27.98", "In stock (18 available)", "Two", "A fascinating fictional portrayal of Anne Morrow, wife of pioneer Charles Lindbergh."),
    ("the-alchemist_958", "The Alchemist", "£38.65", "In stock (18 available)", "Three", "Paulo Coelho's classic parable of Santiago, an Andalusian shepherd boy seeking treasure."),
    ("the-7-habits-of-highly-effective-people_957", "The 7 Habits of Highly Effective People", "£33.16", "In stock (18 available)", "Four", "Stephen R. Covey's timeless framework for personal integrity and professional excellence."),
    ("still-life-with-bread-crumbs_956", "Still Life with Bread Crumbs", "£26.41", "In stock (18 available)", "Three", "An unexpected romance and career renaissance in rural New England."),
    ("slow-hands-stormfront-1_955", "Slow Hands (Stormfront #1)", "£57.55", "In stock (18 available)", "Two", "A fast-paced romance series opener filled with suspense, passion, and high stakes."),
    ("sharp-objects-paperback_954", "Sharp Objects (Paperback)", "£47.82", "In stock (18 available)", "Four", None), # Deliberately missing description for testing
    ("security_953", "Security", "£39.25", "In stock (18 available)", "Two", "A stylish high-concept thriller told through the multiple lenses of a luxury hotel's cameras."),
    ("scarlet-the-lunar-chronicles-2_952", "Scarlet (The Lunar Chronicles #2)", "£14.57", "In stock (18 available)", "Four", "A sci-fi reimagining of Little Red Riding Hood with androids, space battles, and rebellion."),
    ("room_951", "Room", "£22.43", "In stock (18 available)", "One", "Told through the perspective of five-year-old Jack, Room explores survival and devotion."),
    ("ready-player-one_950", "Ready Player One", "£19.07", "In stock (18 available)", "Four", "In the OASIS virtual universe, an epic treasure hunt promises unimaginable wealth."),
    ("proof-of-heaven-a-neurosurgeons-journey-into-the-afterlife_949", "Proof of Heaven: A Neurosurgeon's Journey into the Afterlife", "£51.99", "In stock (18 available)", "Three", "A neurosurgeon's personal account of his near-death experience during a coma."),
    ("pride-and-prejudice_948", "Pride and Prejudice", "£19.20", "In stock (18 available)", "Four", "Jane Austen's masterclass in wit, social nuance, and enduring romance."),
    ("outlander-outlander-1_947", "Outlander (Outlander #1)", "£52.44", "In stock (18 available)", "Five", "Claire Randall is mysteriously hurled back in time to 1743 Scotland and Jamie Fraser."),
    ("no-country-for-old-men_946", "No Country for Old Men", "£39.72", "In stock (18 available)", "One", "Cormac McCarthy's unforgiving, relentless neo-western crime thriller along the Rio Grande."),
    ("night-the-night-trilogy-1_945", "Night (The Night Trilogy #1)", "£13.51", "In stock (18 available)", "One", "Elie Wiesel's unforgettable, devastating memoir of surviving Auschwitz and Buchenwald."),
    ("neither-here-nor-there-travels-in-europe_944", "Neither Here nor There: Travels in Europe", "£38.95", "In stock (18 available)", "Three", "Bill Bryson travels across Europe with signature observational humor and wry observations."),
    ("modern-romance_943", "Modern Romance", "£28.26", "In stock (18 available)", "Five", "Comedian Aziz Ansari teams up with sociologist Eric Klinenberg to study contemporary dating."),
    ("miss-peregrines-home-for-peculiar-children_942", "Miss Peregrine's Home for Peculiar Children", "£10.76", "In stock (18 available)", "One", "A mysterious island orphanage, bizarre vintage photographs, and a haunting adventure."),
    ("looking-for-alaska_941", "Looking for Alaska", "£30.57", "In stock (18 available)", "Three", "Miles Halter heads off to Culver Creek Boarding School seeking a 'Great Perhaps.'")
]

def generate_catalogue_html(page_num: int, books_slice: list, has_next: bool) -> str:
    """Generate HTML for a catalogue page matching Books to Scrape structure."""
    pods = []
    for slug, title, price, avail, rating, _ in books_slice:
        pods.append(f"""
        <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
                <div class="image_container">
                    <a href="{slug}/index.html"><img src="media/cache/placeholder.jpg" alt="{title}" class="thumbnail"></a>
                </div>
                <p class="star-rating {rating}">
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                    <i class="icon-star"></i>
                </p>
                <h3><a href="{slug}/index.html" title="{title}">{title}</a></h3>
                <div class="product_price">
                    <p class="price_color">{price}</p>
                    <p class="instock availability"><i class="icon-ok"></i> {avail}</p>
                    <form><button type="submit" class="btn btn-primary btn-block">Add to basket</button></form>
                </div>
            </article>
        </li>
        """)

    pager_html = ""
    if has_next:
        next_page = page_num + 1
        pager_html = f'<ul class="pager"><li class="next"><a href="page-{next_page}.html">next</a></li></ul>'

    return f"""<!DOCTYPE html>
<html lang="en-us">
<head><title>All products | Books to Scrape - Sandbox</title></head>
<body>
    <div class="container-fluid page">
        <div class="page_inner">
            <ol class="row">
                {"".join(pods)}
            </ol>
            <div>{pager_html}</div>
        </div>
    </div>
</body>
</html>"""

def generate_detail_html(slug: str, title: str, price: str, avail: str, rating: str, desc: str | None) -> str:
    """Generate HTML for a book detail page matching Books to Scrape structure."""
    desc_html = ""
    if desc:
        desc_html = f'<div id="product_description" class="sub-header"><h2>Product Description</h2></div><p>{desc}</p>'

    return f"""<!DOCTYPE html>
<html lang="en-us">
<head><title>{title} | Books to Scrape - Sandbox</title></head>
<body id="default">
    <div class="container-fluid page">
        <div class="page_inner">
            <div id="content_inner">
                <article class="product_page">
                    <div class="row">
                        <div class="col-sm-6 product_main">
                            <h1>{title}</h1>
                            <p class="price_color">{price}</p>
                            <p class="instock availability"><i class="icon-ok"></i> {avail}</p>
                            <p class="star-rating {rating}"><i class="icon-star"></i></p>
                        </div>
                    </div>
                    {desc_html}
                    <div class="sub-header"><h2>Product Information</h2></div>
                    <table class="table table-striped">
                        <tr><th>UPC</th><td>abc123upc</td></tr>
                        <tr><th>Product Type</th><td>Books</td></tr>
                    </table>
                </article>
            </div>
        </div>
    </div>
</body>
</html>"""

def seed_cache_and_fixtures():
    """Populate cache and test fixtures."""
    client = PoliteClient(cache_dir=CACHE_DIR)

    # 1. Seed 3 catalogue pages
    for page_num in range(1, 4):
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
        start_idx = (page_num - 1) * 20
        end_idx = start_idx + 20
        books_slice = BOOKS_DATA[start_idx:end_idx]
        has_next = (page_num < 3)

        html = generate_catalogue_html(page_num, books_slice, has_next)
        cache_path = client._get_cache_path(url)
        cache_path.write_text(html, encoding="utf-8")

    # 2. Seed 60 book detail pages
    for slug, title, price, avail, rating, desc in BOOKS_DATA:
        url = f"https://books.toscrape.com/catalogue/{slug}/index.html"
        html = generate_detail_html(slug, title, price, avail, rating, desc)
        cache_path = client._get_cache_path(url)
        cache_path.write_text(html, encoding="utf-8")

    # 3. Seed offline test fixtures in tests/fixtures
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    # Valid book fixture
    valid_html = generate_detail_html("test-book", "Test Book Title", "£25.50", "In stock (10 available)", "Four", "A test description.")
    (FIXTURES_DIR / "book_valid.html").write_text(valid_html, encoding="utf-8")

    # Missing description fixture
    no_desc_html = generate_detail_html("test-book-no-desc", "Book Without Description", "£12.99", "In stock (5 available)", "Two", None)
    (FIXTURES_DIR / "book_no_desc.html").write_text(no_desc_html, encoding="utf-8")

    # Malformed HTML fixture
    malformed_html = "<html><body><p>Random broken content with no product page</p></body></html>"
    (FIXTURES_DIR / "book_malformed.html").write_text(malformed_html, encoding="utf-8")

    print(f"✅ Successfully seeded {len(BOOKS_DATA)} book details, 3 catalogue pages, and test fixtures!")

if __name__ == "__main__":
    seed_cache_and_fixtures()
