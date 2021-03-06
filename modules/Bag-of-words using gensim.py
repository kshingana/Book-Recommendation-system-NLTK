{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 100,
   "id": "c6b2b19b",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package stopwords to\n",
      "[nltk_data]     C:\\Users\\Kauu\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package stopwords is already up-to-date!\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from nltk.stem import WordNetLemmatizer\n",
    "from nltk.tokenize import word_tokenize\n",
    "import gensim\n",
    "from gensim import corpora\n",
    "from pprint import pprint\n",
    "import string\n",
    "from gensim.utils import simple_preprocess\n",
    "from smart_open import smart_open\n",
    "import nltk\n",
    "nltk.download('stopwords')  # run once\n",
    "from nltk.corpus import stopwords\n",
    "stop_words = stopwords.words('english')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 79,
   "id": "7003a6d1",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ISBN</th>\n",
       "      <th>Book-Title</th>\n",
       "      <th>Book-Author</th>\n",
       "      <th>Year-Of-Publication</th>\n",
       "      <th>Publisher</th>\n",
       "      <th>google_id</th>\n",
       "      <th>book_language</th>\n",
       "      <th>categories</th>\n",
       "      <th>description</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0195153448</td>\n",
       "      <td>Classical Mythology</td>\n",
       "      <td>Mark P. O. Morford</td>\n",
       "      <td>2002</td>\n",
       "      <td>Oxford University Press</td>\n",
       "      <td>KyLfwAEACAAJ</td>\n",
       "      <td>en</td>\n",
       "      <td>Social Science</td>\n",
       "      <td>Provides an introduction to classical myths pl...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0002005018</td>\n",
       "      <td>Clara Callan</td>\n",
       "      <td>Richard Bruce Wright</td>\n",
       "      <td>2001</td>\n",
       "      <td>HarperFlamingo Canada</td>\n",
       "      <td>yfx0vgEACAAJ</td>\n",
       "      <td>en</td>\n",
       "      <td>Actresses</td>\n",
       "      <td>In a small town in Canada, Clara Callan reluct...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0060973129</td>\n",
       "      <td>Decision in Normandy</td>\n",
       "      <td>Carlo D'Este</td>\n",
       "      <td>1991</td>\n",
       "      <td>HarperPerennial</td>\n",
       "      <td>_LufAAAAMAAJ</td>\n",
       "      <td>en</td>\n",
       "      <td>1940-1949</td>\n",
       "      <td>Here, for the first time in paperback, is an o...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0374157065</td>\n",
       "      <td>Flu: The Story of the Great Influenza Pandemic...</td>\n",
       "      <td>Gina Bari Kolata</td>\n",
       "      <td>1999</td>\n",
       "      <td>Farrar Straus Giroux</td>\n",
       "      <td>GkthXOZv17kC</td>\n",
       "      <td>en</td>\n",
       "      <td>Medical</td>\n",
       "      <td>Describes the great flu epidemic of 1918, an o...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>0393045218</td>\n",
       "      <td>The Mummies of Urumchi</td>\n",
       "      <td>E. J. W. Barber</td>\n",
       "      <td>1999</td>\n",
       "      <td>W. W. Norton &amp; Company</td>\n",
       "      <td>5OujQgAACAAJ</td>\n",
       "      <td>en</td>\n",
       "      <td>Design</td>\n",
       "      <td>A look at the incredibly well-preserved ancien...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "         ISBN                                         Book-Title  \\\n",
       "0  0195153448                                Classical Mythology   \n",
       "1  0002005018                                       Clara Callan   \n",
       "2  0060973129                               Decision in Normandy   \n",
       "3  0374157065  Flu: The Story of the Great Influenza Pandemic...   \n",
       "4  0393045218                             The Mummies of Urumchi   \n",
       "\n",
       "            Book-Author  Year-Of-Publication                Publisher  \\\n",
       "0    Mark P. O. Morford                 2002  Oxford University Press   \n",
       "1  Richard Bruce Wright                 2001    HarperFlamingo Canada   \n",
       "2          Carlo D'Este                 1991          HarperPerennial   \n",
       "3      Gina Bari Kolata                 1999     Farrar Straus Giroux   \n",
       "4       E. J. W. Barber                 1999   W. W. Norton & Company   \n",
       "\n",
       "      google_id book_language      categories  \\\n",
       "0  KyLfwAEACAAJ            en  Social Science   \n",
       "1  yfx0vgEACAAJ            en       Actresses   \n",
       "2  _LufAAAAMAAJ            en       1940-1949   \n",
       "3  GkthXOZv17kC            en         Medical   \n",
       "4  5OujQgAACAAJ            en          Design   \n",
       "\n",
       "                                         description  \n",
       "0  Provides an introduction to classical myths pl...  \n",
       "1  In a small town in Canada, Clara Callan reluct...  \n",
       "2  Here, for the first time in paperback, is an o...  \n",
       "3  Describes the great flu epidemic of 1918, an o...  \n",
       "4  A look at the incredibly well-preserved ancien...  "
      ]
     },
     "execution_count": 79,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df = pd.read_csv('description_df_0to100.csv')\n",
    "df.drop(columns = [\"Unnamed: 0\"],inplace=True)\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 80,
   "id": "4a4c2394",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ISBN</th>\n",
       "      <th>Book-Title</th>\n",
       "      <th>Book-Author</th>\n",
       "      <th>Year-Of-Publication</th>\n",
       "      <th>Publisher</th>\n",
       "      <th>google_id</th>\n",
       "      <th>book_language</th>\n",
       "      <th>categories</th>\n",
       "      <th>description</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [ISBN, Book-Title, Book-Author, Year-Of-Publication, Publisher, google_id, book_language, categories, description]\n",
       "Index: []"
      ]
     },
     "execution_count": 80,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#check for NaN values\n",
    "df[df[\"description\"]==\"NaN\"]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 81,
   "id": "f59df977",
   "metadata": {},
   "outputs": [],
   "source": [
    "def remove_punctuation(text):\n",
    "    punctuationfree=\"\".join([i for i in text if i not in string.punctuation])\n",
    "    return punctuationfree"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 82,
   "id": "7e9cab21",
   "metadata": {},
   "outputs": [],
   "source": [
    "doc = []\n",
    "for i in range(len(df)):\n",
    "    if df[\"description\"].loc[i] != \"nan\":\n",
    "        strr = str(df[\"description\"].loc[i]).lower()\n",
    "        doc.append(strr)\n",
    "        #print(strr)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 83,
   "id": "248e2416",
   "metadata": {},
   "outputs": [],
   "source": [
    "#empty_list = pd.DataFrame(empty_list)\n",
    "#.dropna(inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 84,
   "id": "1f594135",
   "metadata": {},
   "outputs": [],
   "source": [
    "#removing NaN values\n",
    "doc = doc[:-12]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 85,
   "id": "324e4073",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['provides an introduction to classical myths placing the addressed topics within their historical context, discussion of archaeological evidence as support for mythical events, and how these themes have been portrayed in literature, art, music, and film.',\n",
       " \"in a small town in canada, clara callan reluctantly takes leave of her sister, nora, who is bound for new york. it's a time when the growing threat of fascism in europe is a constant worry, and people escape from reality through radio and the movies. meanwhile, the two sisters -- vastly different in personality, yet inextricably linked by a shared past -- try to find their places within the complex web of social expectations for young women in the 1930s. while nora embarks on a glamorous career as a radio-soap opera star, clara, a strong and independent-minded woman, struggles to observe the traditional boundaries of a small and tight-knit community without relinquishing her dreams of love, freedom, and adventure. however, things aren't as simple as they appear -- nora's letters eventually reveal life in the big city is less exotic than it seems, and the tranquil solitude of clara's life is shattered by a series of unforeseeable events. these twists of fate require all of clara's courage and strength, and finally put the seemingly unbreakable bond between the sisters to the test.\",\n",
       " 'here, for the first time in paperback, is an outstanding military history that offers a dramatic new perspective on the allied campaign that began with the invasion of the d-day beaches of normandy. nationa advertising in military history.',\n",
       " 'describes the great flu epidemic of 1918, an outbreak that killed some forty million people worldwide, and discusses the efforts of scientists and public health officials to understand and prevent another lethal pandemic',\n",
       " 'a look at the incredibly well-preserved ancient mummies found in western china describes their clothing and appearance, attempts to reconstruct their culture, and speculates about how caucasians could have found their way to the feet of the himalayan mountains.',\n",
       " \"a chinese immigrant who is convinced she is dying threatens to celebrate the chinese new year by unburdening herself of everybody's hidden truths, thus prompting a series of comic misunderstandings\",\n",
       " 'essays by respected military historians, including stephen ambrose, david mccullough, james mcpherson, and john keegan, consider the consequences if history had turned out differently, such as if the weather on d-day had been worse or if washington had not escaped from long island. reprint.',\n",
       " 'now back in print, ann beattie\\'s finest short story collection, reissued to accompany the publication of her latest novel, \"the doctor\\'s house.\" most of the characters in \"where you\\'ll find me\" grew up in the 1960s and 1970s, are in their twenties and thirties and embody a curious, yet familiar, fusion of hope and despair. in finely crafted narratives, beattie writes of women nursing broken hearts, men looking for love, and married couples struggling to stay together.',\n",
       " 'another story based in the fictional rural town in miramichi.',\n",
       " \"based on newly declassified documents and archival research, hitler's secret bankers reveals the full, hitherto unknown extent of swiss economic collaboration with the nazis during world war ii. in this updated edition, readers discover how and why the swiss finally buckled and agreed to pay $1.25 billion in compensation for the funds deposited by holocaust victims in swiss banks. in addition to the dispute over dormant accounts, swiss banks provided to the nazi war machine the foreign currency that paid for vital war materiel such as chrome and aluminum. the author also explains how the exposure of the myth of swiss neutrality, in collaboration with the nazis, triggered investigations into the role of the british regarding holocaust victims and the part played by germany and its failure to compensate the survivors of slave labor, as well as the upheaval in the art world, which failed to restore stolen paintings to their rightful owners.\",\n",
       " 'part dorothy parker, part jose saramago, with shades of george orwell, sheila heti has arrived on canada\\'s literary scene a fully formed artist. balancing wisdom and innocence, joy and foreboding, each story in the middle stories leads us to surprising places. a frog doles out sage advice to a plumber infatuated with a princess, a boy falls hopelessly in love with a monkey, and a man with a hat keeps apocalyptic thoughts at bay by resolving to follow a plan that he admits he won\\'t stick to. globe and mail critic russell smith has described heti\\'s stories as cryptic fairy tales without morals at the end, but really the morals are in the quality of the telling and in the details disclosed along the way. look where you weren\\'t going to look, think what you wouldn\\'t have thought, heti seems to say, and meaning itself gains more meaning and more dimensions. heti\\'s stories are not what you expect, but why did you expect that anyway?\"',\n",
       " 'a collection of inspirational true stories about love, marriage, friendship, overcoming obstacles, and achieving life dreams',\n",
       " 'a beautifully narrated novel of time and place, \"goodbye to the buttermilk sky\" re-creates a southern summer when the depression and the boll weevil turned hopes to dust. with the extraordinary talent to make the reader see the ball canning jars on the kitchen table, hear the clicks on the party line, and feel the bittersweet moments of 20-year-old callie tatum\\'s first experiences with adult desire, oliver portrays a young wife\\'s increasingly dangerous infidelity with cinematic precision and palpable suspense.',\n",
       " \"staring unflinchingly into the abyss of slavery, this novel transforms history into a story as powerful as exodus and as intimate as a lullaby. sethe, its protagonist, was born a slave and escaped to ohio, but eighteen years later she is still not free. she has too many memories of sweet home, the beautiful farm where so many hideous things happened. and sethe's new home is haunted by the ghost of her baby, who died nameless and whose tombstone is engraved with a single word: beloved.\",\n",
       " \"the staff of the onion presents a satirical collection of mock headlines and news stories, including an account of the pentagon's development of an a-bomb-resistant desk for schoolchildren\",\n",
       " \"in new vegetarian celia brooks brown presents an innovative approach to vegetarian cooking. there's practical advice on how to choose and prepare the major vegetarian ingredients, followed by 50 original, stylish recipes, all photographed by philip webb.\",\n",
       " 'provides advice on ways to succeed in business, finance, careers, dating, marriage, school, and getting along with others.',\n",
       " \"problems arise when identical twins emma and sam switch places in order to solve each other's problems, and the girls worry that things will only get worse if the truth about their plan is revealed.\",\n",
       " 'as explained by the kids themselves, this book offers a collection of true stories that deal with moments of embarrassment and awkwardness while providing tips and advice on how to handle such difficult situations when they arise. original.',\n",
       " 'why should i recycle garbage? (pb)',\n",
       " 'wild animus is a search for the primordial, a test of human foundations and a journey to the breaking point.',\n",
       " 'a fatal mid-air collision involving a commercial airliner prompts a frantic, desperate investigation into the causes of the accident, in a thriller exploring the issue of safety and security in the aircraft industry',\n",
       " 'using a quantum time machine, a group of young historians is sent back to the year 1357 to rescue their trapped project leader.',\n",
       " 'dr. ransom is abducted to the eerie red planet, malacandra, where his escape and flight endanger both his life and his chances of ever returning to earth',\n",
       " \"five american expatriates living in budapest in the early 1990s seek to establish themselves and make their fortunes in a city still haunted by the tragedies of its communist past. a first novel. reader's guide included. reprint. 100,000 first printing.\",\n",
       " \"when sydney corbett comes up with the idea of making candy figures of jesus, it's just a business opportunity for him and the people at bea's candies, but it is blasphemy for the reverend willie domingo and the church of the returning vegetarian christ, w\",\n",
       " 'nan',\n",
       " 'die erlebnisse der sch??nen felicia, tochter eines ostpreussischen gutsbesitzers, in den jahren 1914 - 1930.',\n",
       " 'sister john of the cross, an elderly nun, experiences a series of dazzling visions, but she is confronted with a difficult choice between her spiritual gifts and curing the powerful headaches that accompany her visions.',\n",
       " 'the unforgettable novel of a childhood in a sleepy southern town and the crisis of conscience that rocked it, to kill a mockingbird became both an instant bestseller and a critical success when it was first published in 1960. it went on to win the pulitzer prize in 1961 and was later made into an academy award-winning film, also a classic. compassionate, dramatic, and deeply moving, to kill a mockingbird takes readers to the roots of human behavior - to innocence and experience, kindness and cruelty, love and hatred, humor and pathos. now with over 18 million copies in print and translated into forty languages, this regional story by a young alabama woman claims universal appeal. harper lee always considered her book to be a simple love story. today it is regarded as a masterpiece of american literature.',\n",
       " \"an invitation to murder a most unusual death has landed helma zukas right in the middle of another murder scene. stanley plummer has been cataloging a collection of native american books for bellehaven's new cultural center when his body was found in the center's ladies room -- stabbed through his heart, and clutching a barbie doll. miss zukas is asked by the library to finish the cataloging. now she's been asked by the victim -- in a letter dated the day he died -- to get to the bottom of the mystery. unable to resist the urge to dig into the facts, helma becomes convinced there's something hidden in the center that the murderer wants -- and it may be worth killing another cataloger to keep it buried. . .\",\n",
       " \"the year is 1966, a time of innocence, possibility, and freedom. and for atlanta, the country, and one woman making her way in a changing world, nothing will be the same . . . after an airless childhood in savannah, smoky o'donnell arrives in atlanta, dazzled and chastened by this hectic young city on the rise. her new job as a writer with the city's downtown magazine introduces her to many unforgettable people and propels her into the center of momentous events that will irrevocably alter her heart, her career, and her world.\",\n",
       " 'a secret arctic experiment turns into a frozen nightmare when a team of scientists, stranded on a drifting iceberg with a massive explosive charge, battles the elements for survival, only to discover that one of them is a murderer. reissue.',\n",
       " 'koontz looks heavenward for inspiration in his newest suspense thriller, which is chock-full of signs, portents, angels, and one somewhat second-rate devil, a murky and undercharacterized guy named junior cain who throws his beloved wife off a fire tower on an oregon mountain and spends the rest of the novel waiting for the retribution that will surely come. but not before a series of tragedies ensues that convince junior that someone or something named bartholomew is out to exact vengeance for that crime and the series of other murders that follow. --- amazon.',\n",
       " \"angered over the governor's order on speed traps, the eccentric inhabitants of the isle of tangier, off the coast of virginia, declare war on their own state, and it is up to judy hammer, the new superintendent of the state police, to stop the crisis.\",\n",
       " 'presents an anthology of christmas stories reflecting on the various ways in which the holidays serve as a catalyst to promote change, growth, and new beginnings',\n",
       " \"carli d'auber, who has invented a new form of communication that enables people to transfer their consciousness thousands of miles away, finds herself hunted by a conspiracy that wants to use her invention for their own purposes. reprint. lj. k.\",\n",
       " 'the first book in the author\\'s successful \"last days\" series follows a 747 pilot as he tries to recover from the effects of \"the rapture.\" reprint.',\n",
       " 'after a violent encounter with a homeless man, talented corporate lawyer michael finds himself out in the streets, lucky to be alive, and holding a top-secret file belonging to his former employers',\n",
       " 'nan',\n",
       " 'as relevant today as it was 50 years ago, \"all the king\\'s men\" is a classic novel about american politics. set in the 1930s, this pulitzer prize-winning novel traces the rise and fall of demagogue willie stark, a fictional character based on the real-life huey long of louisiana.',\n",
       " 'nan',\n",
       " 'encountering a younger man on a road in italy, seventy-something professor alessandro guiliani recounts his experiences, spinning a tale of love, loss, tragedy, madmen, dwarves, and mafiosi. reprint.',\n",
       " 'based on the simontons\\' experience with hundreds of patients at their world-famous cancer counseling and research center, getting well again introduces the scientific basis for the \"will to live.\" in this revolutionary book the simontons profile the typical \"cancer personality\": how an individual\\'s reactions to stress and other emotional factors can contribute to the onset and progress of cancer -- and how positive expectations, self-awareness, and self-care can contribute to survival. this book offers the same self-help techniques the simonton\\'s patients have used to successfully to reinforce usual medical treatment -- techniques for learning positive attitudes, relaxation, visualization, goal setting, managing pain, exercise, and building an emotional support system.',\n",
       " 'nan',\n",
       " 'ten short stories set in india, dealing with the unpredictable effects of contact between indians and americans.',\n",
       " 'a love story and an epic of the frontier, lonesome dove is the grandest novel ever written about the last, defiant wilderness of america. richly authentic, beautifully written, lonesome dove is a book to make readers laugh, weep, dream and remember. now a blockbuster television event. copyright ?? libri gmbh. all rights reserved.',\n",
       " 'shabanu, a young nomad of the cholistan desert, must submit to the marriage her father arranges for her, or go against centuries of tradition by defying him.',\n",
       " \"having relented to the ways of her people in pakistan and married the rich older man to whom she was pledged against her will, shabanu is now the victim of his family's blood feud and the malice of his other wives\",\n",
       " 'boire un chocolat chaud ou un vin de tokay ?? prague en compagnie de mozart et da ponte, s??journer ?? weimar avec bach et goethe, s\\'envoler pour le japon, atterrir ?? bombay, fl??ner sur l\\'??le saint-louis, cr??er un jardin \" de cur?? \", admirer les cerfs-volants ?? dieppe... autant de promenades, d\\'escapades, de voyages ou de r??cr??ations auxquels nous invite michel tournier avec une gourmandise, une po??sie et un talent jamais d??mentis.',\n",
       " 'dr. carl sagan takes us on a great reading adventure, offering his vivid and startling insight into the brain of man and beast, the origin of human intelligence, the function of our most haunting legends -- and their amazing links to recent discoveries. book jacket.',\n",
       " 'nan',\n",
       " \"encompassing two generations and a rich blend of chinese and american history, the story of four struggling, strong women also reveals their daughters' memories and feelings\",\n",
       " \"generally regarded as the pre-eminent work of conrad's shorter fiction, 'heart of darkness' is a chilling tale of horror which, as the author intended, is capable of many interpretations.\",\n",
       " 'american physician michael aulden stands at the center of an epic global confrontation of the body, mind, and soul, as humankind must choose between the forces of good and evil, with the fate of the entire world at stake. original.',\n",
       " \"the story of a simple country girl whose family's pretentions lead to her destruction\",\n",
       " \"from: venus, goddess of love, 120 main, mt. olympus to: stacy temple, lapsed temptress stacy, stacy, stacy. you were so promising at the beginning: sexy, smart, personable and funny. great on dates and really great afterward-if you know what i mean. but this is a sad state of affairs; or, in your case, non-affairs! it's been nearly an entire year and you haven't had your way with even one eligible male. you've been working so hard concocting sexy lingerie for thongs.com -- and really, stacy, if that little pink velvet bustier didn't put you in the mood, i don't know what to say! -- that you haven't even tried to be coaxed out of your own thong.com! are you listening, stacy? seven days to find the perfect man -- or else! happy hunting!\",\n",
       " \"an expert in chinese philosophy explains facets of taoism using milne's famous character and explores the world of winnie-the-pooh through tao, characterizing pooh as a simple bear who subscribes to the principles of successful living\",\n",
       " 'retraces the journey of seabiscuit, a horse with crooked legs and a pathetic tail that made racing history in 1938, thanks to the efforts of a trainer, owner, and jockey who transformed a bottom-level racehorse into a legend.',\n",
       " 'a collection of advice on how to live a happy and rewarding life.',\n",
       " 'in a futuristic military adventure a recruit goes through the roughest boot camp in the universe and into battle with the terran mobile infantry in what historians would come to call the first interstellar war',\n",
       " 'in nineteenth-century london, sixteen-year-old sally, a recent orphan, becomes involved in a deadly search for a mysterious ruby.',\n",
       " 'a horse in nineteenth-century england recounts his experiences with both good and bad masters.',\n",
       " \"when rape and murder strike young, single women on the sun-drenched san diego coast, police are stumped. one of the victims was dr. cory cohen's patient. the trauma triggers flashbacks of cory's own terrifying rape. her attacker went free, but she vows this one will not. armed with psychological expertise, she is determined to uncover his identity. in her relentless pursuit, she risks the loss of an important friendship, and worse, places herself squarely into the killer's path.\",\n",
       " \"unlike most people matt beckford is actually looking forward to turning thirty. after struggling through most of his twenties he thinks his career, finances and love life are finally sorted. but when he splits up with his girlfriend, he realises that life has different plans for him. unable to cope with his future falling apart matt temporarily moves back to his parents. during his enforced exodus only his old school mates can keep him sane. friends he hasn't seen since he was nineteen. back together after a decade apart. but things will never be the same for any of them because when you're turning thirty nothing's as simple as it used to be.\",\n",
       " \"there is a signal emanating from deep within the ice of antarctica. atlantis has awoken. ancient monuments all over the world - from the pyramids of giza, to mexico, to the ancient sites of china - are also awakening, reacting to a brewing crisis not of this earth, connecting to each other in some kind of ancient global network. a small group of scientists is assembled to attempt to unravel the mystery. what they discover will change the world. imagine that 12,000 years ago it really did rain for 40 days and 40 nights. that storms reigned supreme. imagine that survivors of human civilization really were forced to take to boats or hide out in caves on mountaintops. then consider that these same myths from around the world predict this kind of devastation will occur time and again. what could cause such a catastrophe? what occurs in nature with such frightening and predictable regularity? a pulsar. but this is not just any pulsar - the ordinary type that pulses once a second, a minute, or even a week. this pulses once every 12,000 years and sends out a gravity wave of such ferocity it beggars belief. not only that, it's closer than anybody has ever imagined. for it lives in our own backyard. it is the sun.\",\n",
       " \"the art of being truly funny is an undervalued one in these angst-ridden times, but it is an ability that acclaimed novelist sarah payne stuart has in abundance. her talents have never been on more glorious display than in my first cousin once removed, a memoir--at once hilarious, personal and sad--of her extraordinary boston brahmin family, whose most famous member is the legendary poet robert lowell, the author's first cousin (once removed).\",\n",
       " 'the former vice president and conservative spokesman offers a personal account of his controversial years in the white house, from helping prosecute the war against iraq to starting the \"murphy brown\" debate over family values. 300,000 first printing. $250,000 ad/promo.',\n",
       " 'leadership strategies behind one of the most popular presidents in history how the commander-in-chief commands george w. bush has surprised even his harshest critics with his leadership talents and discipline. as this countrys first mba president, bush formed his unique leadership style managing businesses, not government offices. team bush is the first book to explore these unique methods and tactics he has employed to become one of the nations most popular commanders in chief in recent history. from \"hiring\" the most diverse and effective cabinets in history, to dealing with the crisis and war sparked by the events of september 11th, this compelling leadership book takes readers into the mind and methods of americas 43rd president, and shows managers how these methods can be used to boost productivity in their own organizations. this fast-paced book pulls no punches as it showcases president bushs successes and strengths while detailing his mistakes and weaknesses. focusing on the actual events and outcomes of bushs first two years in office, it discusses: the strategy behind bushs coup in the mid-term election lessons learned from his managing of the september 11th crisis how bush recognizes and learns from his very public mistakes',\n",
       " \"an account of the first year of george w. bush's presidency explores key events, including his controversial election, the september 11th terrorist attack and its aftermath, and their long-term implications for the united states.\",\n",
       " 'tyrel and orrin sackett travel from tennessee to santa fe.',\n",
       " 'the \"brilliant, funny, meaningful novel\" (the new yorker) that established j. d. salinger as a leading voice in american literature--and that has instilled in millions of readers around the world a lifelong love of books. \"if you really want to hear about it, the first thing you\\'ll probably want to know is where i was born, and what my lousy childhood was like, and how my parents were occupied and all before they had me, and all that david copperfield kind of crap, but i don\\'t feel like going into it, if you want to know the truth.\" the hero-narrator of the catcher in the rye is an ancient child of sixteen, a native new yorker named holden caufield. through circumstances that tend to preclude adult, secondhand description, he leaves his prep school in pennsylvania and goes underground in new york city for three days.',\n",
       " 'los ej??rcitos del se??or oscuro van extendiendo cada vez m??s su mal??fica sombra por la tierra media. hombres, elfos y enanos unen sus fuerzas para presentar batalla contra sauron y sus huestes. ajenos a estos preparativos, frodo y sam se internan cada vez m??sen el pa??s de mordor en su heroico viaje para destruir el anillo de poder en las grietas del destino.',\n",
       " 'placed in the federal witness protection program after seeing a murder, manhattan real-estate agent lacey farrell nevertheless must solve the case before she becomes the next victim',\n",
       " 'following her divorce, nell dysart takes a job working for a detective agency and finds herself knee deep in embezzlement, bribery, blackmail, arson, adultery, murder, and passion with her boss, gabe mckenna. 75,000 first printing.',\n",
       " 'when a renowned marriage specialist is publically humiliated by her own straying husband, she fights back by trying to soften the man who made the cover of fortune magazine \"america\\'s toughest bosses\" issue. 65,000 first printing.',\n",
       " 'hailed for its quirkiness and charm, this book tells the story of a new york city lawyer who runs away to a small etruscan village with his wife and baby and discovers a community of eccentrics who make them feel right at home.',\n",
       " 'a priest experiencing a crisis of faith -- and the married woman to whom he is attracted. a scroll newly discovered near jerusalem that, if authentic, could open christianity to a complete reinterpretation. a tragic love affair unfolding in fascist-dominated rome during world war ii. these are the elements of a magnificent literary entertainment -- a novel that resonates with tales of love and betrayal as it deals profoundly with questions of faith and what it means to believe. -- at once a love story, a thriller, and a rich novel of ideas.',\n",
       " 'argues that a good education and a secure job are not guarantees for financial success, and describes six guidelines for making money work for you.',\n",
       " 'set in twelfth-century england, this epic of kings and peasants juxtaposes the building of a magnificent church with the violence and treachery that often characterized the middle ages. reissue.',\n",
       " 'discusses the people, the strategies, and the innovations that turned a hamburger stand into a multi-billion-dollar corporation that revolutionized an industry and influenced the culture of america.',\n",
       " 'reveals natural and effective healing techniques, presents the case stories of seemingly hopeless animal patients, and explains how to stock a homeopathic medicine chest',\n",
       " \"killed in a tragic accident, eddie, an elderly man who believes that he had an uninspired life, awakens in the afterlife, where he discovers that heaven consists of having five people explain the meaning of one's life.\",\n",
       " 'tu nombre escrito en el agua gan?? el xvii premio la sonrisa vertical . su autora, que firma con el seud??nimo de irene gonz??lez frei , acogi??ndose a las bases del premio, ha decidido mantener el anonimato. el fallo del jurado, por primera vez en la historia de este premio, fue un??nime. y no es para menos, ya que nos encontramos ante una primera novela que no s??lo introduce a sus lectores en una hermosa y densa fantas??a er??tica, sino que les revela a una aut??ntica escritora. irene gonz??lez frei dedica su novela a marina , ??de todos los personajes de esta historia el ??nico cuyo nombre no he tenido el valor de cambiar??, y cede la palabra a sof??a para que sea ella la que nos cuente, desde el recuerdo, ??ese amor vertiginoso entre las grietas del dolor y el desconsuelo?? que las unir?? para siempre y fundir?? sus cuerpos, m??s all?? del tenue cristal de los espejos, en el reflejo de narciso. sof??a , una joven al parecer como tantas otras, vive en madrid en el seno de un grupo de amigos que comparten inquietudes y amores. tras el matrimonio con santiago, cuyas relaciones sexuales se extreman en la violencia a medida que el tiempo va corroyendo el afecto y las apetencias, sof??a , desencantada y triste, encuentra un d??a a marina . entre las dos se establece instant??neamente una atracci??n singular, casi m??gica. emprenden un viaje por italia con destino a roma, donde a marina le espera un trabajo en una organizaci??n internacional. poco a poco, de manera irresistible, el lector ir?? impregn??ndose de la progresiva compenetraci??n de las dos mujeres, de la gradual fusi??n de sus cuerpos hasta el punto de que ya no parecen sino una sola. visiones, sue??os, episodios premonitorios van, sin embargo, record??ndole que marina s??lo vive ya en la memoria de sof??a y que una amenaza se cierne sobre ellas. . . la crudeza con que irene gonz??lez frei nos sumerge en los distintos encuentros sexuales no s??lo de las dos mujeres, sino los de ellas con otros personajes, que sirven de contrapunto, invitando al lector a participar directamente de sus tensiones y violencias, de sus goces y delirios, no merma en momento alguno el tono po??tico que envuelve toda la novela y que le otorga la inestimable facultad de dejar una huella indeleble en quienes la leen.',\n",
       " 'the starship enterprise rescues captain montgomery scott, who has been missing in space for seventy-five years and finds that the world has changed beyond his recognition',\n",
       " 'the neglected attendees of the box canyon boys camp find their lives turned around by cotton, who, in a hot-wired pickup, challenges them to join efforts to save a herd of buffalo and rediscover themselves in the process. reissue.',\n",
       " 'when conflicts between rivaling cultures aboard babylon 5 escalate to riotous proportions, security chief garibaldi discovers a link between a station-wide epidemic in nightmares and a strange alien presence. original.',\n",
       " \"peter houston's journey to france to visit the grave of his father, killed in 1944, becomes a nightmare of murder, revenge, deception, and betrayal\"]"
      ]
     },
     "execution_count": 85,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "doc"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 86,
   "id": "cf204c98",
   "metadata": {},
   "outputs": [],
   "source": [
    "list_words = []\n",
    "for i in doc:\n",
    "    temp_1 = (word_tokenize(i))\n",
    "    list_words.append(temp_1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 88,
   "id": "7755506c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['provides',\n",
       " 'an',\n",
       " 'introduction',\n",
       " 'to',\n",
       " 'classical',\n",
       " 'myths',\n",
       " 'placing',\n",
       " 'the',\n",
       " 'addressed',\n",
       " 'topics']"
      ]
     },
     "execution_count": 88,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "list_words[0][:10]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 89,
   "id": "c5db6eae",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import Dictionary\n",
    "from gensim.corpora.dictionary import Dictionary"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 90,
   "id": "ffa304af",
   "metadata": {},
   "outputs": [],
   "source": [
    "#dictionary = corpora.Dictionary(list_words)\n",
    "#print(dictionary.token2id)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 102,
   "id": "c63b5fa4",
   "metadata": {},
   "outputs": [],
   "source": [
    "mydict = corpora.Dictionary([simple_preprocess(line) for line in doc])\n",
    "corpus = [mydict.doc2bow(simple_preprocess(line)) for line in doc]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 103,
   "id": "2bff6f1e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[['addressed', 1], ['an', 1], ['and', 2], ['archaeological', 1], ['art', 1], ['as', 1], ['been', 1], ['classical', 1], ['context', 1], ['discussion', 1], ['events', 1], ['evidence', 1], ['film', 1], ['for', 1], ['have', 1], ['historical', 1], ['how', 1], ['in', 1], ['introduction', 1], ['literature', 1], ['music', 1], ['mythical', 1], ['myths', 1], ['of', 1], ['placing', 1], ['portrayed', 1], ['provides', 1], ['support', 1], ['the', 1], ['their', 1], ['themes', 1], ['these', 1], ['to', 1], ['topics', 1], ['within', 1]]\n",
      "[['and', 8], ['as', 3], ['events', 1], ['for', 2], ['in', 6], ['of', 9], ['the', 11], ['their', 1], ['these', 1], ['to', 3], ['within', 1], ['adventure', 1], ['all', 1], ['appear', 1], ['aren', 1], ['between', 1], ['big', 1], ['bond', 1], ['bound', 1], ['boundaries', 1], ['by', 2], ['callan', 1], ['canada', 1], ['career', 1], ['city', 1], ['clara', 4], ['community', 1], ['complex', 1], ['constant', 1], ['courage', 1], ['different', 1], ['dreams', 1], ['embarks', 1], ['escape', 1], ['europe', 1], ['eventually', 1], ['exotic', 1], ['expectations', 1], ['fascism', 1], ['fate', 1], ['finally', 1], ['find', 1], ['freedom', 1], ['from', 1], ['glamorous', 1], ['growing', 1], ['her', 2], ['however', 1], ['independent', 1], ['inextricably', 1], ['is', 4], ['it', 2], ['knit', 1], ['leave', 1], ['less', 1], ['letters', 1], ['life', 2], ['linked', 1], ['love', 1], ['meanwhile', 1], ['minded', 1], ['movies', 1], ['new', 1], ['nora', 3], ['observe', 1], ['on', 1], ['opera', 1], ['past', 1], ['people', 1], ['personality', 1], ['places', 1], ['put', 1], ['radio', 2], ['reality', 1], ['relinquishing', 1], ['reluctantly', 1], ['require', 1], ['reveal', 1], ['seemingly', 1], ['seems', 1], ['series', 1], ['shared', 1], ['shattered', 1], ['simple', 1], ['sister', 1], ['sisters', 2], ['small', 2], ['soap', 1], ['social', 1], ['solitude', 1], ['star', 1], ['strength', 1], ['strong', 1], ['struggles', 1], ['takes', 1], ['test', 1], ['than', 1], ['they', 1], ['things', 1], ['threat', 1], ['through', 1], ['tight', 1], ['time', 1], ['town', 1], ['traditional', 1], ['tranquil', 1], ['try', 1], ['twists', 1], ['two', 1], ['unbreakable', 1], ['unforeseeable', 1], ['vastly', 1], ['web', 1], ['when', 1], ['while', 1], ['who', 1], ['without', 1], ['woman', 1], ['women', 1], ['worry', 1], ['yet', 1], ['york', 1], ['young', 1]]\n",
      "[['an', 1], ['for', 1], ['in', 2], ['of', 2], ['the', 4], ['is', 1], ['new', 1], ['on', 1], ['time', 1], ['advertising', 1], ['allied', 1], ['beaches', 1], ['began', 1], ['campaign', 1], ['day', 1], ['dramatic', 1], ['first', 1], ['here', 1], ['history', 2], ['invasion', 1], ['military', 2], ['nationa', 1], ['normandy', 1], ['offers', 1], ['outstanding', 1], ['paperback', 1], ['perspective', 1], ['that', 2], ['with', 1]]\n",
      "[['an', 1], ['and', 3], ['of', 2], ['the', 2], ['to', 1], ['people', 1], ['that', 1], ['another', 1], ['describes', 1], ['discusses', 1], ['efforts', 1], ['epidemic', 1], ['flu', 1], ['forty', 1], ['great', 1], ['health', 1], ['killed', 1], ['lethal', 1], ['million', 1], ['officials', 1], ['outbreak', 1], ['pandemic', 1], ['prevent', 1], ['public', 1], ['scientists', 1], ['some', 1], ['understand', 1], ['worldwide', 1]]\n",
      "[['and', 2], ['have', 1], ['how', 1], ['in', 1], ['of', 1], ['the', 3], ['their', 3], ['to', 2], ['describes', 1], ['about', 1], ['ancient', 1], ['appearance', 1], ['at', 1], ['attempts', 1], ['caucasians', 1], ['china', 1], ['clothing', 1], ['could', 1], ['culture', 1], ['feet', 1], ['found', 2], ['himalayan', 1], ['incredibly', 1], ['look', 1], ['mountains', 1], ['mummies', 1], ['preserved', 1], ['reconstruct', 1], ['speculates', 1], ['way', 1], ['well', 1], ['western', 1]]\n",
      "[['of', 2], ['the', 1], ['to', 1], ['by', 1], ['is', 2], ['new', 1], ['series', 1], ['who', 1], ['celebrate', 1], ['chinese', 2], ['comic', 1], ['convinced', 1], ['dying', 1], ['everybody', 1], ['herself', 1], ['hidden', 1], ['immigrant', 1], ['prompting', 1], ['she', 1], ['threatens', 1], ['thus', 1], ['truths', 1], ['unburdening', 1], ['year', 1]]\n",
      "[['and', 1], ['as', 1], ['been', 1], ['the', 2], ['by', 1], ['from', 1], ['on', 1], ['day', 1], ['history', 1], ['military', 1], ['ambrose', 1], ['consequences', 1], ['consider', 1], ['david', 1], ['differently', 1], ['escaped', 1], ['essays', 1], ['had', 3], ['historians', 1], ['if', 3], ['including', 1], ['island', 1], ['james', 1], ['john', 1], ['keegan', 1], ['long', 1], ['mccullough', 1], ['mcpherson', 1], ['not', 1], ['or', 1], ['out', 1], ['reprint', 1], ['respected', 1], ['stephen', 1], ['such', 1], ['turned', 1], ['washington', 1], ['weather', 1], ['worse', 1]]\n",
      "[['and', 5], ['for', 1], ['in', 5], ['of', 4], ['the', 4], ['their', 1], ['to', 2], ['find', 1], ['her', 1], ['love', 1], ['women', 1], ['yet', 1], ['accompany', 1], ['ann', 1], ['are', 1], ['back', 1], ['beattie', 2], ['broken', 1], ['characters', 1], ['collection', 1], ['couples', 1], ['crafted', 1], ['curious', 1], ['despair', 1], ['doctor', 1], ['embody', 1], ['familiar', 1], ['finely', 1], ['finest', 1], ['fusion', 1], ['grew', 1], ['hearts', 1], ['hope', 1], ['house', 1], ['latest', 1], ['ll', 1], ['looking', 1], ['married', 1], ['me', 1], ['men', 1], ['most', 1], ['narratives', 1], ['novel', 1], ['now', 1], ['nursing', 1], ['print', 1], ['publication', 1], ['reissued', 1], ['short', 1], ['stay', 1], ['story', 1], ['struggling', 1], ['thirties', 1], ['together', 1], ['twenties', 1], ['up', 1], ['where', 1], ['writes', 1], ['you', 1]]\n",
      "[['in', 2], ['the', 1], ['town', 1], ['another', 1], ['story', 1], ['based', 1], ['fictional', 1], ['miramichi', 1], ['rural', 1]]\n",
      "[['and', 6], ['art', 1], ['as', 3], ['for', 2], ['how', 2], ['in', 6], ['of', 5], ['the', 17], ['their', 1], ['to', 6], ['by', 2], ['finally', 1], ['on', 1], ['that', 1], ['with', 2], ['well', 1], ['such', 1], ['based', 1], ['accounts', 1], ['addition', 1], ['agreed', 1], ['also', 1], ['aluminum', 1], ['archival', 1], ['author', 1], ['bankers', 1], ['banks', 2], ['billion', 1], ['british', 1], ['buckled', 1], ['chrome', 1], ['collaboration', 2], ['compensate', 1], ['compensation', 1], ['currency', 1], ['declassified', 1], ['deposited', 1], ['discover', 1], ['dispute', 1], ['documents', 1], ['dormant', 1], ['during', 1], ['economic', 1], ['edition', 1], ['explains', 1], ['exposure', 1], ['extent', 1], ['failed', 1], ['failure', 1], ['foreign', 1], ['full', 1], ['funds', 1], ['germany', 1], ['hitherto', 1], ['hitler', 1], ['holocaust', 2], ['ii', 1], ['into', 1], ['investigations', 1], ['its', 1], ['labor', 1], ['machine', 1], ['materiel', 1], ['myth', 1], ['nazi', 1], ['nazis', 2], ['neutrality', 1], ['newly', 1], ['over', 1], ['owners', 1], ['paid', 1], ['paintings', 1], ['part', 1], ['pay', 1], ['played', 1], ['provided', 1], ['readers', 1], ['regarding', 1], ['research', 1], ['restore', 1], ['reveals', 1], ['rightful', 1], ['role', 1], ['secret', 1], ['slave', 1], ['stolen', 1], ['survivors', 1], ['swiss', 5], ['this', 1], ['triggered', 1], ['unknown', 1], ['updated', 1], ['upheaval', 1], ['victims', 2], ['vital', 1], ['war', 3], ['which', 1], ['why', 1], ['world', 2]]\n",
      "[['and', 7], ['as', 1], ['have', 1], ['in', 4], ['of', 2], ['the', 7], ['to', 6], ['by', 1], ['canada', 1], ['love', 1], ['on', 1], ['places', 1], ['seems', 1], ['without', 1], ['that', 2], ['with', 4], ['at', 2], ['look', 2], ['way', 1], ['not', 1], ['out', 1], ['are', 2], ['story', 1], ['where', 1], ['you', 4], ['part', 2], ['why', 1], ['admits', 1], ['advice', 1], ['along', 1], ['anyway', 1], ['apocalyptic', 1], ['arrived', 1], ['artist', 1], ['balancing', 1], ['bay', 1], ['boy', 1], ['but', 2], ['critic', 1], ['cryptic', 1], ['described', 1], ['details', 1], ['did', 1], ['dimensions', 1], ['disclosed', 1], ['doles', 1], ['dorothy', 1], ['each', 1], ['end', 1], ['expect', 2], ['fairy', 1], ['falls', 1], ['follow', 1], ['foreboding', 1], ['formed', 1], ['frog', 1], ['fully', 1], ['gains', 1], ['george', 1], ['globe', 1], ['going', 1], ['has', 2], ['hat', 1], ['he', 2], ['heti', 4], ['hopelessly', 1], ['infatuated', 1], ['innocence', 1], ['itself', 1], ['jose', 1], ['joy', 1], ['keeps', 1], ['leads', 1], ['literary', 1], ['mail', 1], ['man', 1], ['meaning', 2], ['middle', 1], ['monkey', 1], ['morals', 2], ['more', 2], ['orwell', 1], ['parker', 1], ['plan', 1], ['plumber', 1], ['princess', 1], ['quality', 1], ['really', 1], ['resolving', 1], ['russell', 1], ['sage', 1], ['saramago', 1], ['say', 1], ['scene', 1], ['shades', 1], ['sheila', 1], ['smith', 1], ['stick', 1], ['stories', 3], ['surprising', 1], ['tales', 1], ['telling', 1], ['think', 1], ['thought', 1], ['thoughts', 1], ['us', 1], ['weren', 1], ['what', 2], ['wisdom', 1], ['won', 1], ['wouldn', 1]]\n",
      "[['and', 1], ['of', 1], ['dreams', 1], ['life', 1], ['love', 1], ['about', 1], ['collection', 1], ['stories', 1], ['achieving', 1], ['friendship', 1], ['inspirational', 1], ['marriage', 1], ['obstacles', 1], ['overcoming', 1], ['true', 1]]\n",
      "[['and', 4], ['of', 2], ['the', 10], ['to', 3], ['on', 2], ['time', 1], ['when', 1], ['young', 1], ['first', 1], ['with', 3], ['year', 1], ['turned', 1], ['novel', 1], ['adult', 1], ['ball', 1], ['beautifully', 1], ['bittersweet', 1], ['boll', 1], ['buttermilk', 1], ['callie', 1], ['canning', 1], ['cinematic', 1], ['clicks', 1], ['creates', 1], ['dangerous', 1], ['depression', 1], ['desire', 1], ['dust', 1], ['experiences', 1], ['extraordinary', 1], ['feel', 1], ['goodbye', 1], ['hear', 1], ['hopes', 1], ['increasingly', 1], ['infidelity', 1], ['jars', 1], ['kitchen', 1], ['line', 1], ['make', 1], ['moments', 1], ['narrated', 1], ['old', 1], ['oliver', 1], ['palpable', 1], ['party', 1], ['place', 1], ['portrays', 1], ['precision', 1], ['re', 1], ['reader', 1], ['see', 1], ['sky', 1], ['southern', 1], ['summer', 1], ['suspense', 1], ['table', 1], ['talent', 1], ['tatum', 1], ['weevil', 1], ['wife', 1]]\n",
      "[['and', 4], ['as', 4], ['of', 3], ['the', 3], ['to', 1], ['by', 1], ['her', 1], ['is', 3], ['new', 1], ['things', 1], ['who', 1], ['history', 1], ['with', 1], ['she', 2], ['escaped', 1], ['not', 1], ['novel', 1], ['story', 1], ['where', 1], ['into', 2], ['its', 1], ['slave', 1], ['this', 1], ['but', 1], ['has', 1], ['abyss', 1], ['baby', 1], ['beautiful', 1], ['beloved', 1], ['born', 1], ['died', 1], ['eighteen', 1], ['engraved', 1], ['exodus', 1], ['farm', 1], ['free', 1], ['ghost', 1], ['happened', 1], ['haunted', 1], ['hideous', 1], ['home', 2], ['intimate', 1], ['later', 1], ['lullaby', 1], ['many', 2], ['memories', 1], ['nameless', 1], ['ohio', 1], ['powerful', 1], ['protagonist', 1], ['sethe', 2], ['single', 1], ['slavery', 1], ['so', 1], ['staring', 1], ['still', 1], ['sweet', 1], ['tombstone', 1], ['too', 1], ['transforms', 1], ['unflinchingly', 1], ['was', 1], ['whose', 1], ['word', 1], ['years', 1]]\n",
      "[['an', 2], ['and', 1], ['for', 1], ['of', 4], ['the', 3], ['including', 1], ['collection', 1], ['stories', 1], ['account', 1], ['bomb', 1], ['desk', 1], ['development', 1], ['headlines', 1], ['mock', 1], ['news', 1], ['onion', 1], ['pentagon', 1], ['presents', 1], ['resistant', 1], ['satirical', 1], ['schoolchildren', 1], ['staff', 1]]\n",
      "[['an', 1], ['and', 1], ['how', 1], ['in', 1], ['the', 1], ['to', 2], ['all', 1], ['by', 2], ['new', 1], ['on', 1], ['advice', 1], ['presents', 1], ['approach', 1], ['brooks', 1], ['brown', 1], ['celia', 1], ['choose', 1], ['cooking', 1], ['followed', 1], ['ingredients', 1], ['innovative', 1], ['major', 1], ['original', 1], ['philip', 1], ['photographed', 1], ['practical', 1], ['prepare', 1], ['recipes', 1], ['stylish', 1], ['there', 1], ['vegetarian', 3], ['webb', 1]]\n",
      "[['and', 1], ['in', 1], ['provides', 1], ['to', 1], ['on', 1], ['with', 1], ['advice', 1], ['along', 1], ['marriage', 1], ['business', 1], ['careers', 1], ['dating', 1], ['finance', 1], ['getting', 1], ['others', 1], ['school', 1], ['succeed', 1], ['ways', 1]]\n",
      "[['and', 2], ['in', 1], ['the', 2], ['their', 1], ['to', 1], ['is', 1], ['places', 1], ['things', 1], ['when', 1], ['worry', 1], ['that', 1], ['about', 1], ['if', 1], ['worse', 1], ['each', 1], ['plan', 1], ['arise', 1], ['emma', 1], ['get', 1], ['girls', 1], ['identical', 1], ['only', 1], ['order', 1], ['other', 1], ['problems', 2], ['revealed', 1], ['sam', 1], ['solve', 1], ['switch', 1], ['truth', 1], ['twins', 1], ['will', 1]]\n",
      "[['and', 2], ['as', 1], ['how', 1], ['of', 2], ['the', 1], ['to', 1], ['by', 1], ['on', 1], ['they', 1], ['when', 1], ['while', 1], ['offers', 1], ['that', 1], ['with', 1], ['such', 1], ['collection', 1], ['this', 1], ['advice', 1], ['stories', 1], ['true', 1], ['moments', 1], ['original', 1], ['arise', 1], ['awkwardness', 1], ['book', 1], ['deal', 1], ['difficult', 1], ['embarrassment', 1], ['explained', 1], ['handle', 1], ['kids', 1], ['providing', 1], ['situations', 1], ['themselves', 1], ['tips', 1]]\n",
      "[['why', 1], ['garbage', 1], ['pb', 1], ['recycle', 1], ['should', 1]]\n",
      "[['and', 1], ['for', 1], ['of', 1], ['the', 2], ['to', 1], ['is', 1], ['test', 1], ['animus', 1], ['breaking', 1], ['foundations', 1], ['human', 1], ['journey', 1], ['point', 1], ['primordial', 1], ['search', 1], ['wild', 1]]\n",
      "[['and', 1], ['in', 2], ['of', 2], ['the', 4], ['into', 1], ['accident', 1], ['air', 1], ['aircraft', 1], ['airliner', 1], ['causes', 1], ['collision', 1], ['commercial', 1], ['desperate', 1], ['exploring', 1], ['fatal', 1], ['frantic', 1], ['industry', 1], ['investigation', 1], ['involving', 1], ['issue', 1], ['mid', 1], ['prompts', 1], ['safety', 1], ['security', 1], ['thriller', 1]]\n",
      "[['of', 1], ['the', 1], ['their', 1], ['to', 2], ['is', 1], ['time', 1], ['young', 1], ['year', 1], ['historians', 1], ['back', 1], ['machine', 1], ['group', 1], ['leader', 1], ['project', 1], ['quantum', 1], ['rescue', 1], ['sent', 1], ['trapped', 1], ['using', 1]]\n",
      "[['and', 2], ['of', 1], ['the', 1], ['to', 2], ['escape', 1], ['is', 1], ['life', 1], ['where', 1], ['abducted', 1], ['both', 1], ['chances', 1], ['dr', 1], ['earth', 1], ['eerie', 1], ['endanger', 1], ['ever', 1], ['flight', 1], ['his', 3], ['malacandra', 1], ['planet', 1], ['ransom', 1], ['red', 1], ['returning', 1]]\n",
      "[['and', 1], ['in', 3], ['of', 1], ['the', 2], ['their', 1], ['to', 1], ['by', 1], ['city', 1], ['past', 1], ['first', 2], ['reprint', 1], ['novel', 1], ['its', 1], ['make', 1], ['reader', 1], ['haunted', 1], ['still', 1], ['themselves', 1], ['american', 1], ['budapest', 1], ['communist', 1], ['early', 1], ['establish', 1], ['expatriates', 1], ['five', 1], ['fortunes', 1], ['guide', 1], ['included', 1], ['living', 1], ['printing', 1], ['seek', 1], ['tragedies', 1]]\n",
      "[['and', 2], ['for', 2], ['of', 3], ['the', 5], ['is', 1], ['it', 2], ['people', 1], ['when', 1], ['with', 1], ['at', 1], ['up', 1], ['but', 1], ['vegetarian', 1], ['business', 1], ['returning', 1], ['bea', 1], ['blasphemy', 1], ['candies', 1], ['candy', 1], ['christ', 1], ['church', 1], ['comes', 1], ['corbett', 1], ['domingo', 1], ['figures', 1], ['him', 1], ['idea', 1], ['jesus', 1], ['just', 1], ['making', 1], ['opportunity', 1], ['reverend', 1], ['sydney', 1], ['willie', 1]]\n",
      "[['nan', 1]]\n",
      "[['in', 1], ['den', 1], ['der', 1], ['die', 1], ['eines', 1], ['erlebnisse', 1], ['felicia', 1], ['gutsbesitzers', 1], ['jahren', 1], ['ostpreussischen', 1], ['sch??nen', 1], ['tochter', 1]]\n",
      "[['an', 1], ['and', 1], ['of', 2], ['the', 2], ['between', 1], ['her', 2], ['is', 1], ['series', 1], ['sister', 1], ['that', 1], ['with', 1], ['she', 1], ['john', 1], ['accompany', 1], ['but', 1], ['experiences', 1], ['powerful', 1], ['difficult', 1], ['choice', 1], ['confronted', 1], ['cross', 1], ['curing', 1], ['dazzling', 1], ['elderly', 1], ['gifts', 1], ['headaches', 1], ['nun', 1], ['spiritual', 1], ['visions', 2]]\n",
      "[['an', 2], ['and', 9], ['as', 1], ['film', 1], ['in', 4], ['literature', 1], ['of', 4], ['the', 4], ['to', 6], ['by', 1], ['her', 1], ['is', 1], ['it', 4], ['love', 2], ['on', 1], ['simple', 1], ['takes', 1], ['town', 1], ['when', 1], ['woman', 1], ['young', 1], ['dramatic', 1], ['first', 1], ['that', 1], ['with', 1], ['forty', 1], ['million', 1], ['novel', 1], ['now', 1], ['print', 1], ['story', 2], ['also', 1], ['into', 2], ['over', 1], ['readers', 1], ['this', 1], ['innocence', 1], ['southern', 1], ['later', 1], ['was', 2], ['book', 1], ['human', 1], ['both', 1], ['american', 1], ['academy', 1], ['alabama', 1], ['always', 1], ['appeal', 1], ['award', 1], ['be', 1], ['became', 1], ['behavior', 1], ['bestseller', 1], ['childhood', 1], ['claims', 1], ['classic', 1], ['compassionate', 1], ['conscience', 1], ['considered', 1], ['copies', 1], ['crisis', 1], ['critical', 1], ['cruelty', 1], ['deeply', 1], ['experience', 1], ['harper', 1], ['hatred', 1], ['humor', 1], ['instant', 1], ['kill', 2], ['kindness', 1], ['languages', 1], ['lee', 1], ['made', 1], ['masterpiece', 1], ['mockingbird', 2], ['moving', 1], ['pathos', 1], ['prize', 1], ['published', 1], ['pulitzer', 1], ['regarded', 1], ['regional', 1], ['rocked', 1], ['roots', 1], ['sleepy', 1], ['success', 1], ['today', 1], ['translated', 1], ['unforgettable', 1], ['universal', 1], ['went', 1], ['win', 1], ['winning', 1]]\n",
      "[['an', 1], ['and', 2], ['been', 2], ['for', 1], ['in', 4], ['of', 3], ['the', 12], ['to', 7], ['by', 2], ['is', 1], ['it', 2], ['new', 1], ['through', 1], ['when', 1], ['day', 1], ['that', 1], ['another', 2], ['found', 1], ['convinced', 1], ['hidden', 1], ['she', 1], ['collection', 1], ['most', 1], ['now', 1], ['into', 1], ['has', 2], ['he', 1], ['middle', 1], ['scene', 1], ['died', 1], ['was', 1], ['there', 1], ['get', 1], ['his', 2], ['american', 1], ['be', 1], ['asked', 2], ['barbie', 1], ['becomes', 1], ['bellehaven', 1], ['body', 1], ['books', 1], ['bottom', 1], ['buried', 1], ['cataloger', 1], ['cataloging', 2], ['center', 3], ['clutching', 1], ['cultural', 1], ['dated', 1], ['death', 1], ['dig', 1], ['doll', 1], ['facts', 1], ['finish', 1], ['heart', 1], ['helma', 2], ['invitation', 1], ['keep', 1], ['killing', 1], ['ladies', 1], ['landed', 1], ['letter', 1], ['library', 1], ['may', 1], ['miss', 1], ['murder', 2], ['murderer', 1], ['mystery', 1], ['native', 1], ['plummer', 1], ['resist', 1], ['right', 1], ['room', 1], ['something', 1], ['stabbed', 1], ['stanley', 1], ['unable', 1], ['unusual', 1], ['urge', 1], ['victim', 1], ['wants', 1], ['worth', 1], ['zukas', 2]]\n",
      "[['an', 1], ['and', 6], ['as', 1], ['events', 1], ['for', 1], ['in', 3], ['of', 2], ['the', 6], ['to', 1], ['by', 1], ['career', 1], ['city', 2], ['freedom', 1], ['her', 7], ['is', 1], ['new', 1], ['on', 1], ['people', 1], ['time', 1], ['woman', 1], ['young', 1], ['that', 1], ['with', 1], ['way', 1], ['year', 1], ['into', 1], ['this', 1], ['world', 2], ['innocence', 1], ['many', 1], ['will', 2], ['making', 1], ['be', 1], ['childhood', 1], ['unforgettable', 1], ['center', 1], ['heart', 1], ['after', 1], ['airless', 1], ['alter', 1], ['arrives', 1], ['atlanta', 2], ['changing', 1], ['chastened', 1], ['country', 1], ['dazzled', 1], ['donnell', 1], ['downtown', 1], ['hectic', 1], ['introduces', 1], ['irrevocably', 1], ['job', 1], ['magazine', 1], ['momentous', 1], ['nothing', 1], ['one', 1], ['possibility', 1], ['propels', 1], ['rise', 1], ['same', 1], ['savannah', 1], ['smoky', 1], ['writer', 1]]\n",
      "[['for', 1], ['of', 2], ['the', 1], ['to', 1], ['is', 1], ['on', 1], ['when', 1], ['that', 1], ['with', 1], ['scientists', 1], ['discover', 1], ['into', 1], ['secret', 1], ['only', 1], ['murderer', 1], ['one', 1], ['arctic', 1], ['battles', 1], ['charge', 1], ['drifting', 1], ['elements', 1], ['experiment', 1], ['explosive', 1], ['frozen', 1], ['iceberg', 1], ['massive', 1], ['nightmare', 1], ['reissue', 1], ['stranded', 1], ['survival', 1], ['team', 1], ['them', 1], ['turns', 1]]\n",
      "[['an', 1], ['and', 4], ['for', 3], ['in', 1], ['of', 4], ['the', 4], ['to', 1], ['is', 2], ['on', 1], ['series', 2], ['who', 1], ['that', 5], ['not', 1], ['or', 1], ['out', 1], ['novel', 1], ['full', 1], ['which', 1], ['but', 1], ['follow', 1], ['suspense', 1], ['wife', 1], ['beloved', 1], ['other', 1], ['will', 1], ['thriller', 1], ['his', 2], ['tragedies', 1], ['something', 1], ['one', 1], ['amazon', 1], ['angels', 1], ['bartholomew', 1], ['before', 1], ['cain', 1], ['chock', 1], ['come', 1], ['convince', 1], ['crime', 1], ['devil', 1], ['ensues', 1], ['exact', 1], ['fire', 1], ['guy', 1], ['heavenward', 1], ['inspiration', 1], ['junior', 2], ['koontz', 1], ['looks', 1], ['mountain', 1], ['murders', 1], ['murky', 1], ['named', 2], ['newest', 1], ['off', 1], ['oregon', 1], ['portents', 1], ['rate', 1], ['rest', 1], ['retribution', 1], ['second', 1], ['signs', 1], ['someone', 1], ['somewhat', 1], ['spends', 1], ['surely', 1], ['throws', 1], ['tower', 1], ['vengeance', 1], ['waiting', 1]]\n",
      "[['and', 1], ['of', 4], ['the', 7], ['their', 1], ['to', 2], ['is', 1], ['it', 1], ['new', 1], ['on', 2], ['up', 1], ['over', 1], ['war', 1], ['order', 1], ['crisis', 1], ['off', 1], ['angered', 1], ['coast', 1], ['declare', 1], ['eccentric', 1], ['governor', 1], ['hammer', 1], ['inhabitants', 1], ['isle', 1], ['judy', 1], ['own', 1], ['police', 1], ['speed', 1], ['state', 2], ['stop', 1], ['superintendent', 1], ['tangier', 1], ['traps', 1], ['virginia', 1]]\n",
      "[['an', 1], ['and', 1], ['as', 1], ['in', 1], ['of', 1], ['the', 2], ['to', 1], ['new', 1], ['on', 1], ['which', 1], ['stories', 1], ['presents', 1], ['ways', 1], ['anthology', 1], ['beginnings', 1], ['catalyst', 1], ['change', 1], ['christmas', 1], ['growth', 1], ['holidays', 1], ['promote', 1], ['reflecting', 1], ['serve', 1], ['various', 1]]\n",
      "[['for', 1], ['of', 2], ['their', 2], ['to', 2], ['by', 1], ['her', 1], ['new', 1], ['people', 1], ['who', 1], ['that', 2], ['herself', 1], ['reprint', 1], ['has', 1], ['wants', 1], ['own', 1], ['auber', 1], ['away', 1], ['carli', 1], ['communication', 1], ['consciousness', 1], ['conspiracy', 1], ['enables', 1], ['finds', 1], ['form', 1], ['hunted', 1], ['invented', 1], ['invention', 1], ['lj', 1], ['miles', 1], ['purposes', 1], ['thousands', 1], ['transfer', 1], ['use', 1]]\n",
      "[['as', 1], ['in', 1], ['of', 1], ['the', 4], ['to', 1], ['from', 1], ['series', 1], ['first', 1], ['reprint', 1], ['author', 1], ['he', 1], ['book', 1], ['days', 1], ['effects', 1], ['follows', 1], ['last', 1], ['pilot', 1], ['rapture', 1], ['recover', 1], ['successful', 1], ['tries', 1]]\n",
      "[['and', 1], ['in', 1], ['the', 1], ['to', 2], ['with', 1], ['out', 1], ['secret', 1], ['man', 1], ['his', 1], ['be', 1], ['after', 1], ['finds', 1], ['alive', 1], ['belonging', 1], ['corporate', 1], ['employers', 1], ['encounter', 1], ['file', 1], ['former', 1], ['himself', 1], ['holding', 1], ['homeless', 1], ['lawyer', 1], ['lucky', 1], ['michael', 1], ['streets', 1], ['talented', 1], ['top', 1], ['violent', 1]]\n",
      "[['nan', 1]]\n",
      "[['and', 1], ['as', 2], ['in', 1], ['of', 2], ['the', 4], ['all', 1], ['is', 1], ['it', 1], ['life', 1], ['on', 1], ['about', 1], ['long', 1], ['men', 1], ['novel', 2], ['based', 1], ['fictional', 1], ['this', 1], ['was', 1], ['years', 1], ['american', 1], ['willie', 1], ['classic', 1], ['prize', 1], ['pulitzer', 1], ['today', 1], ['winning', 1], ['rise', 1], ['ago', 1], ['character', 1], ['demagogue', 1], ['fall', 1], ['huey', 1], ['king', 1], ['louisiana', 1], ['politics', 1], ['real', 1], ['relevant', 1], ['set', 1], ['stark', 1], ['traces', 1]]\n",
      "[['nan', 1]]\n",
      "[['and', 1], ['in', 1], ['of', 1], ['love', 1], ['on', 1], ['reprint', 1], ['man', 1], ['experiences', 1], ['his', 1], ['something', 1], ['alessandro', 1], ['dwarves', 1], ['encountering', 1], ['guiliani', 1], ['italy', 1], ['loss', 1], ['madmen', 1], ['mafiosi', 1], ['professor', 1], ['recounts', 1], ['road', 1], ['seventy', 1], ['spinning', 1], ['tale', 1], ['tragedy', 1], ['younger', 1]]\n",
      "[['an', 2], ['and', 6], ['for', 2], ['have', 1], ['how', 2], ['in', 1], ['of', 2], ['support', 1], ['the', 8], ['their', 1], ['to', 6], ['expectations', 1], ['on', 1], ['personality', 1], ['offers', 1], ['with', 1], ['at', 1], ['well', 1], ['based', 1], ['research', 1], ['this', 2], ['world', 1], ['getting', 1], ['other', 1], ['will', 1], ['book', 2], ['experience', 1], ['center', 1], ['introduces', 1], ['same', 1], ['survival', 1], ['again', 1], ['attitudes', 1], ['awareness', 1], ['basis', 1], ['building', 1], ['can', 2], ['cancer', 3], ['care', 1], ['contribute', 2], ['counseling', 1], ['emotional', 2], ['exercise', 1], ['factors', 1], ['famous', 1], ['goal', 1], ['help', 1], ['hundreds', 1], ['individual', 1], ['learning', 1], ['live', 1], ['managing', 1], ['medical', 1], ['onset', 1], ['pain', 1], ['patients', 2], ['positive', 2], ['profile', 1], ['progress', 1], ['reactions', 1], ['reinforce', 1], ['relaxation', 1], ['revolutionary', 1], ['scientific', 1], ['self', 3], ['setting', 1], ['simonton', 1], ['simontons', 2], ['stress', 1], ['successfully', 1], ['system', 1], ['techniques', 2], ['treatment', 1], ['typical', 1], ['used', 1], ['usual', 1], ['visualization', 1]]\n",
      "[['nan', 1]]\n",
      "[['and', 1], ['in', 1], ['of', 1], ['the', 1], ['between', 1], ['with', 1], ['short', 1], ['stories', 1], ['effects', 1], ['set', 1], ['americans', 1], ['contact', 1], ['dealing', 1], ['india', 1], ['indians', 1], ['ten', 1], ['unpredictable', 1]]\n",
      "[['an', 1], ['and', 2], ['of', 2], ['the', 3], ['to', 1], ['all', 1], ['is', 2], ['love', 1], ['about', 1], ['novel', 1], ['now', 1], ['story', 1], ['readers', 1], ['beautifully', 1], ['make', 1], ['book', 1], ['ever', 1], ['last', 1], ['america', 1], ['authentic', 1], ['blockbuster', 1], ['copyright', 1], ['defiant', 1], ['dove', 2], ['dream', 1], ['epic', 1], ['event', 1], ['frontier', 1], ['gmbh', 1], ['grandest', 1], ['laugh', 1], ['libri', 1], ['lonesome', 2], ['remember', 1], ['reserved', 1], ['richly', 1], ['rights', 1], ['television', 1], ['weep', 1], ['wilderness', 1], ['written', 2]]\n",
      "[['for', 1], ['of', 2], ['the', 2], ['to', 1], ['by', 1], ['her', 2], ['young', 1], ['or', 1], ['marriage', 1], ['him', 1], ['against', 1], ['arranges', 1], ['centuries', 1], ['cholistan', 1], ['defying', 1], ['desert', 1], ['father', 1], ['go', 1], ['must', 1], ['nomad', 1], ['shabanu', 1], ['submit', 1], ['tradition', 1]]\n",
      "[['and', 2], ['in', 1], ['of', 3], ['the', 4], ['to', 2], ['her', 2], ['is', 1], ['people', 1], ['she', 1], ['married', 1], ['now', 1], ['man', 1], ['was', 1], ['ways', 1], ['other', 1], ['will', 1], ['his', 2], ['victim', 1], ['against', 1], ['shabanu', 1], ['blood', 1], ['family', 1], ['feud', 1], ['having', 1], ['malice', 1], ['older', 1], ['pakistan', 1], ['pledged', 1], ['relented', 1], ['rich', 1], ['whom', 1], ['wives', 1]]\n",
      "[['talent', 1], ['admirer', 1], ['atterrir', 1], ['autant', 1], ['auxquels', 1], ['avec', 2], ['bach', 1], ['boire', 1], ['bombay', 1], ['cerfs', 1], ['chaud', 1], ['chocolat', 1], ['compagnie', 1], ['cr??er', 1], ['cur??', 1], ['da', 1], ['de', 6], ['dieppe', 1], ['d??mentis', 1], ['en', 1], ['envoler', 1], ['escapades', 1], ['et', 3], ['fl??ner', 1], ['goethe', 1], ['gourmandise', 1], ['invite', 1], ['jamais', 1], ['japon', 1], ['jardin', 1], ['le', 1], ['les', 1], ['louis', 1], ['michel', 1], ['mozart', 1], ['nous', 1], ['ou', 2], ['ponte', 1], ['pour', 1], ['po??sie', 1], ['prague', 1], ['promenades', 1], ['r??cr??ations', 1], ['saint', 1], ['sur', 1], ['s??journer', 1], ['tokay', 1], ['tournier', 1], ['un', 4], ['une', 2], ['vin', 1], ['volants', 1], ['voyages', 1], ['weimar', 1], ['??le', 1]]\n",
      "[['and', 3], ['of', 3], ['the', 3], ['their', 1], ['to', 1], ['adventure', 1], ['on', 1], ['takes', 1], ['great', 1], ['most', 1], ['into', 1], ['man', 1], ['us', 1], ['book', 1], ['human', 1], ['dr', 1], ['his', 1], ['amazing', 1], ['beast', 1], ['brain', 1], ['carl', 1], ['discoveries', 1], ['function', 1], ['haunting', 1], ['insight', 1], ['intelligence', 1], ['jacket', 1], ['legends', 1], ['links', 1], ['offering', 1], ['origin', 1], ['our', 1], ['reading', 1], ['recent', 1], ['sagan', 1], ['startling', 1], ['vivid', 1]]\n",
      "[['nan', 1]]\n",
      "[['and', 3], ['of', 2], ['the', 1], ['their', 1], ['strong', 1], ['two', 1], ['women', 1], ['history', 1], ['chinese', 1], ['story', 1], ['struggling', 1], ['also', 1], ['reveals', 1], ['memories', 1], ['american', 1], ['rich', 1], ['blend', 1], ['daughters', 1], ['encompassing', 1], ['feelings', 1], ['four', 1], ['generations', 1]]\n",
      "[['as', 2], ['of', 4], ['the', 2], ['is', 2], ['author', 1], ['which', 1], ['many', 1], ['regarded', 1], ['heart', 1], ['tale', 1], ['capable', 1], ['chilling', 1], ['conrad', 1], ['darkness', 1], ['eminent', 1], ['fiction', 1], ['generally', 1], ['horror', 1], ['intended', 1], ['interpretations', 1], ['pre', 1], ['shorter', 1], ['work', 1]]\n",
      "[['an', 1], ['and', 2], ['as', 1], ['of', 4], ['the', 5], ['between', 1], ['fate', 1], ['with', 1], ['at', 2], ['world', 1], ['choose', 1], ['original', 1], ['american', 1], ['body', 1], ['center', 1], ['michael', 1], ['epic', 1], ['must', 1], ['aulden', 1], ['confrontation', 1], ['entire', 1], ['evil', 1], ['forces', 1], ['global', 1], ['good', 1], ['humankind', 1], ['mind', 1], ['physician', 1], ['soul', 1], ['stake', 1], ['stands', 1]]\n",
      "[['of', 1], ['the', 1], ['to', 1], ['her', 1], ['simple', 1], ['story', 1], ['whose', 1], ['country', 1], ['family', 1], ['destruction', 1], ['girl', 1], ['lead', 1], ['pretentions', 1]]\n",
      "[['an', 1], ['and', 4], ['been', 2], ['for', 1], ['in', 2], ['of', 3], ['the', 3], ['to', 4], ['find', 1], ['from', 1], ['is', 1], ['it', 1], ['love', 1], ['on', 1], ['put', 1], ['that', 2], ['with', 1], ['great', 2], ['at', 1], ['way', 1], ['year', 1], ['had', 1], ['if', 2], ['or', 2], ['out', 1], ['are', 1], ['you', 7], ['this', 1], ['but', 1], ['man', 1], ['really', 2], ['say', 1], ['what', 2], ['so', 2], ['be', 1], ['one', 1], ['own', 1], ['state', 1], ['days', 1], ['entire', 1], ['affairs', 2], ['afterward', 1], ['beginning', 1], ['bustier', 1], ['case', 1], ['coaxed', 1], ['com', 2], ['concocting', 1], ['dates', 1], ['didn', 1], ['don', 1], ['eligible', 1], ['else', 1], ['even', 2], ['funny', 1], ['goddess', 1], ['happy', 1], ['hard', 1], ['haven', 2], ['hunting', 1], ['know', 2], ['lapsed', 1], ['lingerie', 1], ['listening', 1], ['little', 1], ['main', 1], ['male', 1], ['mean', 1], ['mood', 1], ['mt', 1], ['nearly', 1], ['non', 1], ['olympus', 1], ['perfect', 1], ['personable', 1], ['pink', 1], ['promising', 1], ['sad', 1], ['seven', 1], ['sexy', 2], ['smart', 1], ['stacy', 6], ['temple', 1], ['temptress', 1], ['thong', 1], ['thongs', 1], ['tried', 1], ['ve', 1], ['velvet', 1], ['venus', 1], ['were', 1], ['working', 1], ['your', 3]]\n",
      "[['an', 1], ['and', 1], ['as', 1], ['in', 1], ['of', 3], ['the', 3], ['to', 1], ['simple', 1], ['through', 1], ['who', 1], ['chinese', 1], ['explains', 1], ['world', 1], ['using', 1], ['living', 1], ['successful', 1], ['character', 1], ['famous', 1], ['bear', 1], ['characterizing', 1], ['expert', 1], ['explores', 1], ['facets', 1], ['milne', 1], ['philosophy', 1], ['pooh', 2], ['principles', 1], ['subscribes', 1], ['tao', 1], ['taoism', 1], ['winnie', 1]]\n",
      "[['and', 2], ['in', 1], ['of', 2], ['the', 2], ['to', 1], ['who', 1], ['history', 1], ['that', 1], ['with', 1], ['efforts', 1], ['into', 1], ['journey', 1], ['made', 1], ['bottom', 1], ['crooked', 1], ['horse', 1], ['jockey', 1], ['legend', 1], ['legs', 1], ['level', 1], ['owner', 1], ['pathetic', 1], ['racehorse', 1], ['racing', 1], ['retraces', 1], ['seabiscuit', 1], ['tail', 1], ['thanks', 1], ['trainer', 1], ['transformed', 1]]\n",
      "[['and', 1], ['how', 1], ['of', 1], ['to', 1], ['life', 1], ['on', 1], ['collection', 1], ['advice', 1], ['live', 1], ['happy', 1], ['rewarding', 1]]\n",
      "[['and', 1], ['in', 3], ['the', 4], ['to', 1], ['adventure', 1], ['through', 1], ['first', 1], ['military', 1], ['with', 1], ['historians', 1], ['into', 1], ['war', 1], ['what', 1], ['come', 1], ['battle', 1], ['boot', 1], ['call', 1], ['camp', 1], ['futuristic', 1], ['goes', 1], ['infantry', 1], ['interstellar', 1], ['mobile', 1], ['recruit', 1], ['roughest', 1], ['terran', 1], ['universe', 1], ['would', 1]]\n",
      "[['for', 1], ['in', 2], ['year', 1], ['old', 1], ['search', 1], ['becomes', 1], ['recent', 1], ['century', 1], ['deadly', 1], ['involved', 1], ['london', 1], ['mysterious', 1], ['nineteenth', 1], ['orphan', 1], ['ruby', 1], ['sally', 1], ['sixteen', 1]]\n",
      "[['and', 1], ['in', 1], ['with', 1], ['experiences', 1], ['both', 1], ['his', 1], ['recounts', 1], ['good', 1], ['horse', 1], ['century', 1], ['nineteenth', 1], ['bad', 1], ['england', 1], ['masters', 1]]\n",
      "[['an', 1], ['and', 2], ['in', 1], ['of', 3], ['the', 5], ['to', 1], ['her', 2], ['is', 1], ['on', 1], ['places', 1], ['when', 1], ['women', 1], ['young', 1], ['with', 1], ['herself', 1], ['she', 3], ['not', 1], ['worse', 1], ['are', 1], ['into', 1], ['this', 1], ['victims', 1], ['but', 1], ['friendship', 1], ['free', 1], ['single', 1], ['was', 1], ['will', 1], ['dr', 1], ['his', 1], ['went', 1], ['murder', 1], ['one', 2], ['coast', 1], ['own', 1], ['police', 1], ['loss', 1], ['armed', 1], ['attacker', 1], ['cohen', 1], ['cory', 2], ['determined', 1], ['diego', 1], ['drenched', 1], ['expertise', 1], ['flashbacks', 1], ['identity', 1], ['important', 1], ['killer', 1], ['path', 1], ['patient', 1], ['psychological', 1], ['pursuit', 1], ['rape', 2], ['relentless', 1], ['risks', 1], ['san', 1], ['squarely', 1], ['strike', 1], ['stumped', 1], ['sun', 1], ['terrifying', 1], ['trauma', 1], ['triggers', 1], ['uncover', 1], ['vows', 1]]\n",
      "[['and', 1], ['as', 2], ['for', 2], ['of', 2], ['the', 1], ['to', 4], ['career', 1], ['different', 1], ['finally', 1], ['is', 1], ['it', 1], ['life', 2], ['love', 1], ['people', 1], ['simple', 1], ['things', 1], ['through', 1], ['when', 2], ['that', 1], ['with', 2], ['are', 1], ['back', 2], ['looking', 1], ['most', 2], ['struggling', 1], ['together', 1], ['twenties', 1], ['up', 1], ['you', 1], ['during', 1], ['but', 2], ['has', 1], ['he', 5], ['old', 1], ['re', 1], ['exodus', 1], ['was', 1], ['school', 1], ['only', 1], ['will', 1], ['his', 7], ['him', 2], ['be', 2], ['keep', 1], ['unable', 1], ['after', 2], ['nothing', 1], ['same', 1], ['them', 1], ['can', 1], ['used', 1], ['actually', 1], ['any', 1], ['apart', 2], ['because', 1], ['beckford', 1], ['cope', 1], ['decade', 1], ['enforced', 1], ['falling', 1], ['finances', 1], ['forward', 1], ['friends', 1], ['future', 1], ['girlfriend', 1], ['hasn', 1], ['mates', 1], ['matt', 2], ['moves', 1], ['never', 1], ['nineteen', 1], ['parents', 1], ['plans', 1], ['realises', 1], ['sane', 1], ['seen', 1], ['since', 1], ['sorted', 1], ['splits', 1], ['temporarily', 1], ['thinks', 1], ['thirty', 2], ['turning', 2], ['unlike', 1]]\n",
      "[['and', 4], ['for', 2], ['in', 4], ['myths', 1], ['of', 9], ['the', 9], ['these', 1], ['to', 8], ['within', 1], ['all', 1], ['from', 3], ['is', 4], ['it', 5], ['on', 1], ['small', 1], ['than', 1], ['they', 1], ['time', 1], ['that', 6], ['with', 1], ['scientists', 1], ['some', 1], ['ancient', 3], ['china', 1], ['could', 1], ['consider', 1], ['not', 3], ['or', 2], ['out', 2], ['such', 3], ['are', 1], ['also', 1], ['discover', 1], ['over', 1], ['survivors', 1], ['this', 4], ['world', 3], ['but', 1], ['did', 1], ['each', 1], ['has', 2], ['really', 2], ['what', 3], ['years', 2], ['there', 1], ['only', 1], ['other', 1], ['will', 2], ['human', 1], ['group', 1], ['earth', 1], ['ever', 1], ['just', 1], ['crisis', 1], ['mystery', 1], ['same', 1], ['second', 1], ['own', 1], ['change', 1], ['days', 1], ['ago', 1], ['again', 1], ['our', 1], ['global', 1], ['even', 1], ['were', 1], ['sun', 1], ['any', 1], ['antarctica', 1], ['anybody', 1], ['around', 1], ['assembled', 1], ['atlantis', 1], ['attempt', 1], ['awakening', 1], ['awoken', 1], ['backyard', 1], ['beggars', 1], ['belief', 1], ['boats', 1], ['brewing', 1], ['catastrophe', 1], ['cause', 1], ['caves', 1], ['civilization', 1], ['closer', 1], ['connecting', 1], ['deep', 1], ['devastation', 1], ['emanating', 1], ['every', 1], ['ferocity', 1], ['forced', 1], ['frightening', 1], ['giza', 1], ['gravity', 1], ['hide', 1], ['ice', 1], ['imagine', 2], ['imagined', 1], ['kind', 2], ['lives', 1], ['mexico', 1], ['minute', 1], ['monuments', 1], ['mountaintops', 1], ['nature', 1], ['network', 1], ['nights', 1], ['occur', 1], ['occurs', 1], ['once', 2], ['ordinary', 1], ['predict', 1], ['predictable', 1], ['pulsar', 2], ['pulses', 2], ['pyramids', 1], ['rain', 1], ['reacting', 1], ['regularity', 1], ['reigned', 1], ['sends', 1], ['signal', 1], ['sites', 1], ['storms', 1], ['supreme', 1], ['take', 1], ['then', 1], ['type', 1], ['unravel', 1], ['wave', 1], ['week', 1]]\n",
      "[['an', 2], ['and', 1], ['art', 1], ['been', 1], ['have', 1], ['in', 3], ['of', 2], ['the', 3], ['these', 1], ['her', 2], ['is', 3], ['it', 1], ['on', 1], ['than', 1], ['first', 2], ['that', 1], ['at', 1], ['most', 1], ['author', 1], ['but', 1], ['has', 1], ['more', 1], ['extraordinary', 1], ['whose', 1], ['one', 1], ['famous', 1], ['family', 1], ['funny', 1], ['sad', 1], ['never', 1], ['once', 3], ['ability', 1], ['abundance', 1], ['acclaimed', 1], ['angst', 1], ['being', 1], ['boston', 1], ['brahmin', 1], ['cousin', 2], ['display', 1], ['glorious', 1], ['hilarious', 1], ['legendary', 1], ['lowell', 1], ['member', 1], ['memoir', 1], ['my', 1], ['novelist', 1], ['payne', 1], ['personal', 1], ['poet', 1], ['removed', 2], ['ridden', 1], ['robert', 1], ['sarah', 1], ['stuart', 1], ['talents', 1], ['times', 1], ['truly', 1], ['undervalued', 1]]\n",
      "[['and', 1], ['in', 1], ['of', 1], ['the', 4], ['to', 1], ['from', 1], ['first', 1], ['offers', 1], ['house', 1], ['over', 1], ['war', 1], ['years', 1], ['account', 1], ['brown', 1], ['his', 1], ['printing', 1], ['former', 1], ['against', 1], ['family', 1], ['personal', 1], ['ad', 1], ['conservative', 1], ['controversial', 1], ['debate', 1], ['helping', 1], ['iraq', 1], ['murphy', 1], ['president', 1], ['promo', 1], ['prosecute', 1], ['spokesman', 1], ['starting', 1], ['values', 1], ['vice', 1], ['white', 1]]\n",
      "[['and', 10], ['as', 2], ['events', 2], ['how', 3], ['in', 8], ['of', 6], ['the', 12], ['their', 1], ['these', 2], ['to', 4], ['by', 1], ['from', 3], ['is', 1], ['it', 2], ['on', 1], ['takes', 1], ['two', 1], ['while', 1], ['first', 3], ['history', 3], ['with', 2], ['discusses', 1], ['public', 1], ['not', 1], ['most', 3], ['into', 1], ['readers', 1], ['this', 3], ['war', 1], ['formed', 1], ['george', 1], ['has', 2], ['he', 1], ['years', 1], ['book', 3], ['mid', 1], ['his', 6], ['be', 1], ['crisis', 2], ['one', 2], ['team', 1], ['own', 1], ['can', 1], ['managing', 2], ['used', 1], ['dealing', 1], ['recent', 1], ['mind', 1], ['even', 1], ['talents', 1], ['president', 3], ['actual', 1], ['americas', 1], ['become', 1], ['behind', 2], ['boost', 1], ['bush', 4], ['bushs', 3], ['businesses', 1], ['cabinets', 1], ['chief', 2], ['commander', 1], ['commanders', 1], ['commands', 1], ['compelling', 1], ['countrys', 1], ['coup', 1], ['critics', 1], ['detailing', 1], ['discipline', 1], ['diverse', 1], ['effective', 1], ['election', 1], ['employed', 1], ['explore', 1], ['fast', 1], ['focusing', 1], ['government', 1], ['harshest', 1], ['hiring', 1], ['leadership', 4], ['learned', 1], ['learns', 1], ['lessons', 1], ['managers', 1], ['mba', 1], ['methods', 3], ['mistakes', 2], ['nations', 1], ['no', 1], ['office', 1], ['offices', 1], ['organizations', 1], ['outcomes', 1], ['paced', 1], ['popular', 2], ['presidents', 1], ['productivity', 1], ['pulls', 1], ['punches', 1], ['rd', 1], ['recognizes', 1], ['september', 2], ['showcases', 1], ['shows', 1], ['sparked', 1], ['strategies', 1], ['strategy', 1], ['strengths', 1], ['style', 1], ['successes', 1], ['surprised', 1], ['tactics', 1], ['term', 1], ['th', 2], ['unique', 2], ['very', 1], ['weaknesses', 1]]\n",
      "[['an', 1], ['and', 2], ['events', 1], ['for', 1], ['of', 2], ['the', 3], ['their', 1], ['first', 1], ['year', 1], ['including', 1], ['long', 1], ['its', 1], ['george', 1], ['account', 1], ['his', 1], ['explores', 1], ['controversial', 1], ['bush', 1], ['election', 1], ['september', 1], ['term', 1], ['th', 1], ['aftermath', 1], ['attack', 1], ['implications', 1], ['key', 1], ['presidency', 1], ['states', 1], ['terrorist', 1], ['united', 1]]\n",
      "[['and', 1], ['to', 1], ['from', 1], ['fe', 1], ['orrin', 1], ['sackett', 1], ['santa', 1], ['tennessee', 1], ['travel', 1], ['tyrel', 1]]\n",
      "[['an', 1], ['and', 6], ['as', 1], ['for', 1], ['how', 1], ['in', 5], ['literature', 1], ['of', 5], ['the', 8], ['to', 4], ['all', 2], ['city', 1], ['is', 2], ['it', 2], ['love', 1], ['new', 3], ['they', 1], ['through', 1], ['york', 1], ['first', 1], ['that', 4], ['about', 1], ['ancient', 1], ['david', 1], ['had', 1], ['if', 2], ['ll', 1], ['me', 1], ['novel', 1], ['where', 1], ['you', 3], ['into', 1], ['readers', 1], ['world', 1], ['but', 1], ['going', 1], ['has', 1], ['he', 1], ['really', 1], ['what', 1], ['adult', 1], ['feel', 1], ['hear', 1], ['born', 1], ['was', 2], ['school', 1], ['truth', 1], ['his', 1], ['american', 1], ['childhood', 1], ['books', 1], ['native', 1], ['before', 1], ['named', 1], ['days', 1], ['don', 1], ['funny', 1], ['know', 2], ['were', 1], ['goes', 1], ['sixteen', 1], ['parents', 1], ['around', 1], ['kind', 1], ['my', 2], ['brilliant', 1], ['catcher', 1], ['caufield', 1], ['child', 1], ['circumstances', 1], ['copperfield', 1], ['crap', 1], ['description', 1], ['established', 1], ['hero', 1], ['holden', 1], ['instilled', 1], ['leading', 1], ['leaves', 1], ['lifelong', 1], ['like', 2], ['lousy', 1], ['meaningful', 1], ['millions', 1], ['narrator', 1], ['occupied', 1], ['pennsylvania', 1], ['preclude', 1], ['prep', 1], ['probably', 1], ['rye', 1], ['salinger', 1], ['secondhand', 1], ['tend', 1], ['thing', 1], ['three', 1], ['underground', 1], ['voice', 1], ['want', 3], ['yorker', 2]]\n",
      "[['sam', 1], ['de', 2], ['en', 2], ['ajenos', 1], ['anillo', 1], ['batalla', 1], ['cada', 2], ['contra', 1], ['del', 2], ['destino', 1], ['destruir', 1], ['ej??rcitos', 1], ['el', 2], ['elfos', 1], ['enanos', 1], ['estos', 1], ['extendiendo', 1], ['frodo', 1], ['fuerzas', 1], ['grietas', 1], ['heroico', 1], ['hombres', 1], ['huestes', 1], ['internan', 1], ['la', 1], ['las', 1], ['los', 1], ['mal??fica', 1], ['media', 1], ['mordor', 1], ['m??s', 1], ['m??sen', 1], ['oscuro', 1], ['para', 2], ['pa??s', 1], ['poder', 1], ['por', 1], ['preparativos', 1], ['presentar', 1], ['sauron', 1], ['se', 1], ['se??or', 1], ['sombra', 1], ['su', 2], ['sus', 2], ['tierra', 1], ['unen', 1], ['van', 1], ['vez', 2], ['viaje', 1]]\n",
      "[['in', 1], ['the', 3], ['she', 1], ['solve', 1], ['becomes', 1], ['murder', 1], ['victim', 1], ['after', 1], ['before', 1], ['real', 1], ['must', 1], ['case', 1], ['agent', 1], ['estate', 1], ['farrell', 1], ['federal', 1], ['lacey', 1], ['manhattan', 1], ['nevertheless', 1], ['next', 1], ['placed', 1], ['program', 1], ['protection', 1], ['seeing', 1], ['witness', 1]]\n",
      "[['and', 2], ['for', 1], ['in', 1], ['her', 2], ['takes', 1], ['first', 1], ['with', 1], ['herself', 1], ['printing', 1], ['murder', 1], ['job', 1], ['finds', 1], ['working', 1], ['deep', 1], ['adultery', 1], ['agency', 1], ['arson', 1], ['blackmail', 1], ['boss', 1], ['bribery', 1], ['detective', 1], ['divorce', 1], ['dysart', 1], ['embezzlement', 1], ['following', 1], ['gabe', 1], ['knee', 1], ['mckenna', 1], ['nell', 1], ['passion', 1]]\n",
      "[['of', 1], ['the', 2], ['to', 1], ['by', 2], ['her', 1], ['is', 1], ['when', 1], ['who', 1], ['first', 1], ['she', 1], ['back', 1], ['man', 1], ['marriage', 1], ['issue', 1], ['printing', 1], ['made', 1], ['magazine', 1], ['own', 1], ['america', 1], ['bosses', 1], ['cover', 1], ['fights', 1], ['fortune', 1], ['humiliated', 1], ['husband', 1], ['publically', 1], ['renowned', 1], ['soften', 1], ['specialist', 1], ['straying', 1], ['toughest', 1], ['trying', 1]]\n",
      "[['and', 3], ['for', 1], ['of', 2], ['the', 1], ['to', 1], ['city', 1], ['community', 1], ['new', 1], ['small', 1], ['who', 2], ['york', 1], ['with', 1], ['at', 1], ['story', 1], ['its', 1], ['this', 1], ['feel', 1], ['make', 1], ['wife', 1], ['baby', 1], ['home', 1], ['book', 1], ['his', 1], ['right', 1], ['them', 1], ['away', 1], ['lawyer', 1], ['charm', 1], ['discovers', 1], ['eccentrics', 1], ['etruscan', 1], ['hailed', 1], ['quirkiness', 1], ['runs', 1], ['tells', 1], ['village', 1]]\n",
      "[['and', 4], ['as', 1], ['in', 1], ['of', 5], ['the', 2], ['these', 1], ['to', 3], ['is', 1], ['it', 2], ['love', 3], ['woman', 1], ['that', 2], ['with', 2], ['at', 1], ['could', 1], ['if', 1], ['are', 1], ['married', 1], ['novel', 2], ['story', 1], ['during', 1], ['ii', 1], ['newly', 1], ['war', 1], ['world', 1], ['he', 1], ['literary', 1], ['tales', 1], ['what', 1], ['thriller', 1], ['crisis', 1], ['elements', 1], ['authentic', 1], ['rich', 1], ['whom', 1], ['once', 1], ['affair', 1], ['attracted', 1], ['believe', 1], ['betrayal', 1], ['christianity', 1], ['complete', 1], ['deals', 1], ['discovered', 1], ['dominated', 1], ['entertainment', 1], ['experiencing', 1], ['faith', 2], ['fascist', 1], ['ideas', 1], ['jerusalem', 1], ['magnificent', 1], ['means', 1], ['near', 1], ['open', 1], ['priest', 1], ['profoundly', 1], ['questions', 1], ['resonates', 1], ['rome', 1], ['scroll', 1], ['tragic', 1], ['unfolding', 1]]\n",
      "[['and', 2], ['for', 3], ['that', 1], ['describes', 1], ['not', 1], ['are', 1], ['you', 1], ['making', 1], ['success', 1], ['job', 1], ['work', 1], ['good', 1], ['argues', 1], ['education', 1], ['financial', 1], ['guarantees', 1], ['guidelines', 1], ['money', 1], ['secure', 1], ['six', 1]]\n",
      "[['and', 2], ['in', 1], ['of', 2], ['the', 3], ['that', 1], ['with', 1], ['this', 1], ['middle', 1], ['church', 1], ['reissue', 1], ['set', 1], ['building', 1], ['epic', 1], ['century', 1], ['england', 1], ['magnificent', 1], ['ages', 1], ['characterized', 1], ['juxtaposes', 1], ['kings', 1], ['often', 1], ['peasants', 1], ['treachery', 1], ['twelfth', 1], ['violence', 1]]\n",
      "[['an', 1], ['and', 2], ['of', 1], ['the', 4], ['people', 1], ['that', 2], ['discusses', 1], ['culture', 1], ['turned', 1], ['billion', 1], ['into', 1], ['industry', 1], ['america', 1], ['strategies', 1], ['corporation', 1], ['dollar', 1], ['hamburger', 1], ['influenced', 1], ['innovations', 1], ['multi', 1], ['revolutionized', 1], ['stand', 1]]\n",
      "[['and', 2], ['how', 1], ['of', 1], ['the', 1], ['to', 1], ['seemingly', 1], ['explains', 1], ['reveals', 1], ['stories', 1], ['presents', 1], ['patients', 1], ['techniques', 1], ['case', 1], ['effective', 1], ['animal', 1], ['chest', 1], ['healing', 1], ['homeopathic', 1], ['hopeless', 1], ['medicine', 1], ['natural', 1], ['stock', 1]]\n",
      "[['an', 2], ['in', 2], ['of', 2], ['the', 2], ['life', 2], ['people', 1], ['who', 1], ['that', 2], ['killed', 1], ['had', 1], ['where', 1], ['he', 2], ['man', 1], ['meaning', 1], ['accident', 1], ['five', 1], ['elderly', 1], ['one', 1], ['having', 1], ['discovers', 1], ['tragic', 1], ['afterlife', 1], ['awakens', 1], ['believes', 1], ['consists', 1], ['eddie', 1], ['explain', 1], ['heaven', 1], ['uninspired', 1]]\n",
      "[['he', 1], ['de', 22], ['en', 12], ['le', 2], ['les', 1], ['un', 4], ['no', 6], ['del', 4], ['destino', 1], ['el', 17], ['grietas', 1], ['la', 12], ['las', 7], ['los', 4], ['m??s', 1], ['para', 3], ['por', 2], ['se', 3], ['su', 2], ['sus', 5], ['van', 1], ['vez', 1], ['viaje', 1], ['acogi??ndose', 1], ['afecto', 1], ['agua', 1], ['al', 2], ['alguno', 1], ['all??', 1], ['amenaza', 1], ['amigos', 1], ['amor', 1], ['amores', 1], ['anonimato', 1], ['ante', 1], ['apetencias', 1], ['atracci??n', 1], ['autora', 1], ['aut??ntica', 1], ['bases', 1], ['cambiar', 1], ['casi', 1], ['cede', 1], ['cierne', 1], ['como', 1], ['comparten', 1], ['compenetraci??n', 1], ['con', 5], ['contrapunto', 1], ['corroyendo', 1], ['cristal', 1], ['crudeza', 1], ['cuente', 1], ['cuerpos', 2], ['cuyas', 1], ['cuyo', 1], ['decidido', 1], ['dedica', 1], ['dejar', 1], ['delirios', 1], ['densa', 1], ['desconsuelo', 1], ['desde', 1], ['desencantada', 1], ['directamente', 1], ['distintos', 1], ['dolor', 1], ['donde', 1], ['dos', 3], ['d??a', 1], ['ella', 1], ['ellas', 2], ['embargo', 1], ['emprenden', 1], ['encontramos', 1], ['encuentra', 1], ['encuentros', 1], ['entre', 2], ['envuelve', 1], ['episodios', 1], ['er??tica', 1], ['es', 1], ['escrito', 1], ['escritora', 1], ['ese', 1], ['espejos', 1], ['espera', 1], ['esta', 1], ['establece', 1], ['este', 1], ['extreman', 1], ['facultad', 1], ['fallo', 1], ['fantas??a', 1], ['firma', 1], ['frei', 3], ['fue', 1], ['fundir??', 1], ['fusi??n', 1], ['gan??', 1], ['goces', 1], ['gonz??lez', 3], ['gradual', 1], ['grupo', 1], ['ha', 1], ['hasta', 1], ['hermosa', 1], ['historia', 2], ['huella', 1], ['impregn??ndose', 1], ['indeleble', 1], ['inestimable', 1], ['inquietudes', 1], ['internacional', 1], ['introduce', 1], ['invitando', 1], ['irene', 3], ['irresistible', 1], ['ir??', 1], ['italia', 1], ['joven', 1], ['jurado', 1], ['lector', 2], ['lectores', 1], ['leen', 1], ['madrid', 1], ['manera', 1], ['mantener', 1], ['marina', 4], ['matrimonio', 1], ['medida', 1], ['memoria', 1], ['menos', 1], ['merma', 1], ['momento', 1], ['mujeres', 2], ['m??gica', 1], ['narciso', 1], ['nombre', 2], ['nos', 3], ['novela', 3], ['organizaci??n', 1], ['otorga', 1], ['otras', 1], ['otros', 1], ['palabra', 1], ['parecen', 1], ['parecer', 1], ['participar', 1], ['personajes', 2], ['poco', 2], ['po??tico', 1], ['premio', 3], ['premonitorios', 1], ['primera', 2], ['progresiva', 1], ['punto', 1], ['que', 16], ['quienes', 1], ['record??ndole', 1], ['recuerdo', 1], ['reflejo', 1], ['relaciones', 1], ['revela', 1], ['roma', 1], ['santiago', 1], ['sea', 1], ['seno', 1], ['seud??nimo', 1], ['sexuales', 2], ['siempre', 1], ['sin', 1], ['singular', 1], ['sino', 3], ['sirven', 1], ['sobre', 1], ['sof??a', 4], ['sola', 1], ['sonrisa', 1], ['sue??os', 1], ['sumerge', 1], ['s??lo', 3], ['tantas', 1], ['tenido', 1], ['tensiones', 1], ['tenue', 1], ['tiempo', 1], ['toda', 1], ['todos', 1], ['tono', 1], ['trabajo', 1], ['tras', 1], ['triste', 1], ['tu', 1], ['una', 9], ['unir??', 1], ['un??nime', 1], ['va', 1], ['valor', 1], ['vertical', 1], ['vertiginoso', 1], ['violencia', 1], ['violencias', 1], ['visiones', 1], ['vive', 2], ['xvii', 1], ['ya', 3], ['??nico', 1]]\n",
      "[['and', 1], ['been', 1], ['for', 1], ['in', 1], ['the', 2], ['who', 1], ['that', 1], ['world', 1], ['has', 2], ['years', 1], ['his', 1], ['five', 1], ['finds', 1], ['seventy', 1], ['beyond', 1], ['captain', 1], ['changed', 1], ['enterprise', 1], ['missing', 1], ['montgomery', 1], ['recognition', 1], ['rescues', 1], ['scott', 1], ['space', 1], ['starship', 1]]\n",
      "[['and', 1], ['in', 2], ['of', 2], ['the', 3], ['their', 1], ['to', 2], ['by', 1], ['find', 1], ['who', 1], ['efforts', 1], ['turned', 1], ['themselves', 1], ['reissue', 1], ['them', 1], ['camp', 1], ['around', 1], ['lives', 1], ['attendees', 1], ['box', 1], ['boys', 1], ['buffalo', 1], ['canyon', 1], ['challenges', 1], ['cotton', 1], ['herd', 1], ['hot', 1], ['join', 1], ['neglected', 1], ['pickup', 1], ['process', 1], ['rediscover', 1], ['save', 1], ['wired', 1]]\n",
      "[['and', 1], ['in', 1], ['to', 1], ['between', 2], ['when', 1], ['epidemic', 1], ['original', 1], ['security', 1], ['chief', 1], ['discovers', 1], ['aboard', 1], ['alien', 1], ['babylon', 1], ['conflicts', 1], ['cultures', 1], ['escalate', 1], ['garibaldi', 1], ['link', 1], ['nightmares', 1], ['presence', 1], ['proportions', 1], ['riotous', 1], ['rivaling', 1], ['station', 1], ['strange', 1], ['wide', 1]]\n",
      "[['and', 1], ['in', 1], ['of', 2], ['the', 1], ['to', 2], ['killed', 1], ['journey', 1], ['his', 1], ['becomes', 1], ['murder', 1], ['nightmare', 1], ['father', 1], ['betrayal', 1], ['deception', 1], ['france', 1], ['grave', 1], ['houston', 1], ['peter', 1], ['revenge', 1], ['visit', 1]]\n"
     ]
    }
   ],
   "source": [
    "# Show the Word Weights in Corpus\n",
    "for doc in corpus:\n",
    "    print([[mydict[id], freq] for id, freq in doc])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 108,
   "id": "ef5943ed",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save the Dict and Corpus\n",
    "mydict.save('mydict.dict')  # save dict to disk\n",
    "corpora.MmCorpus.serialize('bow_corpus.mm', bow_corpus)  # save corpus to disk"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 109,
   "id": "e54d7e3b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load them back\n",
    "loaded_dict = corpora.Dictionary.load('mydict.dict')\n",
    "corpus = corpora.MmCorpus('bow_corpus.mm')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
