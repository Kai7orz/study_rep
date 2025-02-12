//親要素の文字を，より小さな領域の子要素の始点の位置に合わせる
//方法について調べる




class Word{
    constructor(word, defintion, pictureUrl){
        this.word = word;
        this.defintion = defintion;
        this.pictureUrl = pictureUrl;
    }
}

class EmotionObject{
    constructor(emotion, description, color, onomatopoeia){
        this.emotion = emotion;
        this.description = description;
        this.color = color;
        this.onomatopoeia = onomatopoeia;
    }

    getOnomatopoeiaWords(){
        let myWords = []
    for (const i of this.onomatopoeia){
        let myword = new Word(i,dictionary[i],pictureDictionary[i]);
        myWords.push(myword);
        } 
    return myWords 
    }

    getHtmlContainerString(){
// containerSectionに対してHTMLを設定します。
let containerSection = "<div>";
    containerSection +=
    `
        <div id="sec${this.word}" class="bg-${this.color} ">
            <h2>${this.emotion}</h2>
            <p>${this.description}</p>
        </div>
    `;
    containerSection += "</div>";
    let parent = document.getElementById(`"sec${this.word}"`);
    parent.append(makeCards(this.getOnomatopoeiaWords()));
     //makeCardsは感情のカードをまとめて<div>に入れて返す関数
     //呼び出し側では引数のwordオブジェクトのword,deifinition,imgをよびだして配置して，divでまとめればいいだけ
}

}

//グローバル定数
const emoFaces = {
    "surprised":"🤨",
    "fearful":"🥲",
    "angry":"😡",
    "happy":"🥰",
    "bad":"😱",
    "sad":"😿",
    "disgusted":"😟"
}

const emoColor = {
    "surprised":"bg-primary",
    "fearful":"bg-info",
    "angry":"bg-danger",
    "happy":"bg-warning",
    "sad":"bg-secondary",
    "bad":"bg-dark",
    "disgusted":"bg-success"
}

const dictionary = {
    "bark":"the sound made by a dog",
    "grunt":"issue a low, animal-like noise",
    "roar":"make a loud noise, as of an animal",
    "whack":"the act of hitting vigorously",
    "smack":"a blow from a flat object (as an open hand)",
    "hiss":`make a sharp, elongated "s" sound`,
    "ahem":"the utterance of a sound similar to clearing the throat",
    "bawl":"cry loudly",
    "bling":"flashy, ostentatious jewelry",
    "boom":"a deep prolonged loud noise",
    "buzz":"the sound of rapid vibration",
    "caw":"utter a cry, characteristic of crows, rooks, or ravens",
    "chatter":"talk socially without exchanging too much information",
    "chant":"a repetitive song in which syllables are assigned to a tone",
    "clatter":"a continuous rattling sound as of hard objects falling or striking each other.",
    "clunk":"a heavy dull sound (as made by impact of heavy objects)",
    "crawl":"move forward on the hands and knees or by dragging the body close to the ground.",
    "flick":"throw or toss with a quick motion",
    "giggle":"a light, silly laugh.",
    "gargle":"an act or instance or the sound of washing one's mouth and throat with a liquid kept in motion by exhaling through it.",
    "honk":"the cry of a goose or any loud sound resembling it",
    "oink":"the short low gruff noise of the kind made by hogs",
    "whine":"a complaint uttered in a plaintive way",
    "waah":"sound made when crying by babies",
    "zing":"sound my by something energetic"
};

const pictureDictionary = {
    "bark":"https://cdn.pixabay.com/photo/2013/07/25/11/59/german-shepherd-166972_1280.jpg",
    "grunt":"https://cdn.pixabay.com/photo/2010/11/29/nepal-419__480.jpg",
    "roar":"https://cdn.pixabay.com/photo/2018/04/13/21/24/lion-3317670_1280.jpg",
    "whack":"https://cdn.pixabay.com/photo/2017/10/27/11/49/boxer-2894025_1280.jpg",
    "smack":"https://cdn.pixabay.com/photo/2015/03/20/19/38/hammer-682767_1280.jpg",
    "hiss":"https://cdn.pixabay.com/photo/2016/10/13/23/30/cat-1739091_1280.jpg",
    "ahem":"https://cdn.pixabay.com/photo/2014/03/13/10/12/man-286476_1280.jpg",
    "bawl":"https://cdn.pixabay.com/photo/2015/06/26/10/17/smiley-822365_960_720.jpg",
    "bling":"https://cdn.pixabay.com/photo/2017/12/30/13/37/happy-new-year-3050088_1280.jpg",
    "boom":"https://cdn.pixabay.com/photo/2016/04/12/21/17/explosion-1325471_1280.jpg",
    "buzz":"https://cdn.pixabay.com/photo/2020/02/13/10/29/bees-4845211_1280.jpg",
    "caw":"https://cdn.pixabay.com/photo/2017/02/16/11/13/bird-2071185_1280.jpg",
    "chatter":"https://cdn.pixabay.com/photo/2014/07/25/08/55/bar-401546_1280.jpg",
    "chant":"https://cdn.pixabay.com/photo/2016/07/19/07/43/parchment-1527650__340.jpg",
    "clatter":"https://cdn.pixabay.com/photo/2020/02/06/19/01/clutter-4825256_1280.jpg",
    "clunk":"https://cdn.pixabay.com/photo/2017/01/10/03/06/steel-1968194_1280.jpg",
    "crawl":"https://cdn.pixabay.com/photo/2017/11/23/07/47/baby-2972221__340.jpg",
    "flick":"https://cdn.pixabay.com/photo/2012/02/23/08/48/disgust-15793_1280.jpg",
    "giggle":"https://cdn.pixabay.com/photo/2017/08/07/15/18/people-2604850_1280.jpg",
    "gargle":"https://cdn.pixabay.com/photo/2017/04/03/16/32/girl-smoke-cigarette-2198839_1280.jpg",
    "honk":"https://cdn.pixabay.com/photo/2017/02/28/14/37/geese-2105918_1280.jpg",
    "oink":"https://cdn.pixabay.com/photo/2019/03/02/15/32/pig-4030013_1280.jpg",
    "whine":"https://cdn.pixabay.com/photo/2020/05/01/01/57/girl-5115192_960_720.jpg",
    "waah":"https://cdn.pixabay.com/photo/2017/01/18/02/18/emotions-1988745_1280.jpg",
    "zing":"https://cdn.pixabay.com/photo/2017/09/14/16/38/fiber-optic-2749588_1280.jpg"
};

const emotions = [
    new EmotionObject("angry", "feeling or showing strong annoyance, displeasure, or hostility; full of anger.", "red", ["bark","grunt", "roar","whack","smack","hiss"]),
    new EmotionObject("happy", "feeling or showing pleasure or contentment.", "yellow", ["bling","chatter","chant","giggle"]),
    new EmotionObject("bad", "not such as to be hoped for or desired; unpleasant or unwelcome.", "beige", ["ahem","clatter","clunk"]),
    new EmotionObject("sad", "feeling or showing sorrow; unhappy.", "grey", ["bawl","whine","waah"]),
    new EmotionObject("surprised", "to feel mild astonishment or shock.", "purple", ["boom","honk","zing"]),
    new EmotionObject("fearful", "feeling afraid; showing fear or anxiety.", "green", ["buzz","caw","crawl"]),
    new EmotionObject("disgusted", "feeling or showing strong annoyance, displeasure, or hostility; full of anger.", "orange", ["flick","gargle","oink"])
];


/*
1つのwordクラスに含まれる，すべての擬音に対応する説明カードを作成
    入力:擬音を含むWordクラスの配列
*/ 

function makeCards(words){
//今使ってない

    //作成した複数のカードを保持すためのコンテナ
    let cardsContainer = document.createElement("div");
    let cardsContainerRow = document.createElement("div");
    cardsContainer.classList.add("container");
    cardsContainerRow.classList.add("row");


    //カード1枚


    for(w in words){
        let card = document.createElement("div");
        //        card.classList.add("bg-white","d-flex","justify-content-between","m-2");
        card.classList.add("col-md-4","col-12","m-2");
        let sentence = document.createElement("p");
        sentence.innerHTML = w.word + "<br>" + w.defintion;
        let conImg = document.createElement("img");
        conImg.src = w.pictureUrl;
        card.append(sentence);
        card.append(conImg);
        cardsContainerRow.append(card);        
    }

    cardsContainer.append(cardsContainerRow);
    return cardsContainer;
}

function makeBottomCards(){
    let eleCounter = 0;


    let finalContainer = document.createElement("div");

    while(1){
        if(eleCounter >= emotions.length){
            break;
        }

        let tempContainer = document.createElement("div");
      
        tempContainer.classList.add(emoColor[emotions[eleCounter].emotion]);
        let sentenceGroup = document.createElement("div");
        let emoHeader = document.createElement("h2");
        let sen = document.createElement("p1");
        let cardsHolder = document.createElement("div");
        let cRow = document.createElement("div");
        cardsHolder.classList.add("container");
        cRow.classList.add("row");
        

        emoHeader.innerHTML = emotions[eleCounter].emotion;
        sen.innerHTML = emotions[eleCounter].description;

        //tempContainer.append(emoHeader);
        //tempContainer.append(sentenceGroup);

        let tempDiv = document.createElement("div");
        tempDiv.classList.add("d-flex","flex-column","text-white","mb-3","w-100");
        tempDiv.append(emoHeader);
        tempDiv.append(sen);

        cRow.append(tempDiv);
        for( ono of emotions[eleCounter].getOnomatopoeiaWords()){
        //擬音語含むword配列を取得しfor文で回していく
        //音ごとにカードを作成する必要がある
        let tempCard = document.createElement("div");
        //tempCard.classList.add("d-flex","justify-content-between","w-75","mx-auto","my-3","bg-white");
        tempCard.classList.add("col-md-5","col-10","w-50","mx-auto","my-2","bg-white");

        let oneCard = document.createElement("div");
        oneCard.classList.add("d-flex","justify-content-between","align-items-center","p-3");

        let tempImg = document.createElement("img");
        tempImg.src = ono.pictureUrl;
        tempImg.classList.add("h-25","w-25","m-1");
        let tempSentenceGroup = document.createElement("div");
        let tempHeader = document.createElement("h3");
        let tempSentence = document.createElement("p");
        tempHeader.innerHTML = ono.word;
        tempSentence.innerHTML = ono.defintion;

        tempSentenceGroup.append(tempHeader);
        tempSentenceGroup.append(tempSentence);

        oneCard.append(tempSentenceGroup);
        oneCard.append(tempImg);

        tempCard.append(oneCard);

        cRow.append(tempCard);
        }

        cardsHolder.append(cRow);
        let myId = "sec"+emotions[eleCounter].emotion;
        tempContainer.setAttribute("id","sec"+ emotions[eleCounter].emotion);
        eleCounter++;
        tempContainer.append(cardsHolder);
        //secangryとかがid名
        finalContainer.append(tempContainer);
    }

        return finalContainer;
}


let emoName = [];

for( emo of emotions){
    emoName.push(emo.emotion);
}




let emoContainer = document.createElement("div");
emoContainer.classList.add("container");
let ContainerRow = document.createElement("div");
ContainerRow.classList.add("row");

let myCounter = 0;

while(1){

    let siege = document.createElement("a");
    siege.href = "#sec"+emotions[myCounter].emotion;
    siege.style.textDecoration = 'none';
    if(myCounter < emotions.length){        


    let emoCardsContainer = document.createElement("div");
    emoCardsContainer.classList.add("col-12","col-md-4","mx-auto","m-4");
    let mycard = document.createElement("div");
    mycard.classList.add("d-flex","flex-column","text-center","justify-content-center",emoColor[emoName[myCounter]],"w-100","h-100","mx-auto","mb-4");

    let eName = document.createElement("h3");
    let emoFace = document.createElement("p");
    let emoSentence = document.createElement("p");

    eName.classList.add("text-white");
    emoFace.classList.add("m-3","text-center","display-4");
    emoSentence.classList.add("text-white");

    eName.innerHTML = emoName[myCounter];
    emoFace.innerHTML = emoFaces[emoName[myCounter]];
    emoSentence.innerHTML = emotions[myCounter].description;


    mycard.append(eName);
    mycard.append(emoFace);
    mycard.append(emoSentence);
    siege.append(mycard);
    emoCardsContainer.append(siege);
    ContainerRow.append(emoCardsContainer);
    myCounter++;
    }


    
    if(myCounter >= emotions.length){
        break;
    }
}

emoContainer.append(ContainerRow);

let pageRoot = document.getElementById("target");
pageRoot.append(emoContainer);

pageRoot.append(makeBottomCards());