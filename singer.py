
#read file until eof/digit/alphabet
def readChar(file):
    while True:
        c = file.read(1)
        if not c:
            print("EOF")
            return None
        else:
            if c.isdigit():
                return c
            elif c.isalpha():
                return c
            elif c=='.' or c=='+' or c=='-' or c=='>' or c=='<':
                return c

def peekChar(file):
    pos = file.tell()
    data = charRead(file) # Might try/except this line, and finally: f.seek(pos)
    file.seek(pos)
    return data
def unReadChar(file):
    pos = file.tell()
    file.seek(pos-1)
    #return data


octave = 0
noteLength=4
#returns chroma,length,dot,finflg
def parseNext(file):
    global noteLength
    global octave
    soundflag=False
    charRead=""
    chroma=0;
    noteSymbol = 0;
    finflg = False

    #breakflag=False
    dot=False

    while True:
        charRead=readChar(file);
        #print(charRead)
        #end of file
        if charRead == None:
            finflg = true
            break

        if charRead== 'c':
            if soundflag == False:
                soundflag=True
                chroma = 3 + (octave-1) * 12;
            else: # //soundflag==1 既に一度音を読んでいる場合
                unReadChar(file)
                break
        elif charRead== 'd':
            if soundflag== False:
                soundflag=True
                chroma= 5 + (octave-1)*12;
            else: # soundflag==1 既に一度音を読んでいる場合
                unReadChar(file)
                break
        elif charRead== 'e':
            if soundflag== False:
                soundflag=True
                chroma= 7 + (octave-1)*12;
            else: # soundflag==1 既に一度音を読んでいる場合
                unReadChar(file)
                break
        elif charRead== 'f':
            if soundflag== False:
                soundflag=True
                chroma= 8 + (octave-1)*12;
            else: #soundflag==1 既に一度音を読んでいる場合
                unReadChar(file)
                break
        elif charRead== 'g':
            if soundflag== False:
                soundflag=True
                chroma= 10 + (octave-1)*12;
            else: #soundflag==1 既に一度音を読んでいる場合
                unReadChar(file)
                break
        elif charRead== 'a':
            if soundflag== False:
                soundflag=True
                #chroma= 0 + (octave-1)*12;
                chroma= 12 + (octave-1)*12;
            else: #soundflag==1 既に一度音を読んでいる場合
                unReadChar(file)
                break
        elif charRead== 'b':
            if soundflag== False:
                soundflag=True
                #chroma= 2 + (octave-1)*12;
                chroma= 14 + (octave-1)*12;
            else: #soundflag==1 既に一度音を読んでいる場合
                unReadChar(file)
                break
        elif charRead== 'r':
            if soundflag== False:
                soundflag=True
                chroma= -1
            else: #soundflag==1 既に一度音を読んでいる場合
                unReadChar(file)
                break
        elif charRead== 'o' or charRead == 'O':
            if soundflag==False:
                charRead = readChar(file)
                octave = int(charRead)
            else:
                unReadChar(file)
                break

        elif charRead == '<':#//ascii 60
            if soundflag == False:
                octave = octave - 1
            else:
                unReadChar(file)
                break
        elif charRead== '>':#//ascii 62
            if soundflag == False:
                octave = octave + 1
            else:
                unReadChar(file)
                break
        elif charRead== '2':
            noteSymbol=2
        elif charRead== '4':
            noteSymbol=4
        elif charRead== '8':
            noteSymbol=8;
        elif charRead== '6':
            noteSymbol=16;
        elif charRead== '1':
            charRead = readChar(file)
            if charRead =='6':
                noteSymbol=16
            elif charRead == '2':
                noteSymbol=12
            else:
                unReadChar(file)
                noteSymbol=1;
        elif charRead== 'l':
            if soundflag == True:
                unReadChar(file)
                break
            else:
                charRead=readChar(file)
                if charRead== '1':
                    charRead = readChar(file)#stringcharReadAt(line,++index)=='6'){
                    if charRead == '6':
                        noteLength=16
                    elif charRead == '2':
                        noteLength=12
                    else:
                        unReadChar(file)
                        noteLength=1
                elif charRead== '2':
                    noteLength=2;
                elif charRead== '4':
                    noteLength=4;
                elif charRead== '8':
                    noteLength=8;
        elif charRead== '+':
            chroma = chroma + 1
        elif charRead== '-':
            chroma = chroma - 1
        elif charRead== '.':
            dot = True;
        elif charRead== 'S':
            readChar(file)
            readChar(file)
            readChar(file)

        elif charRead== '}':
            readChar(file)
            readChar(file)
    if noteSymbol != 0:
        length = noteSymbol
    else:
        length = noteLength
    return chroma,length,dot,finflg


"""
char stringcharReadAt(String line,int index){
	char output;
        try {
          output = line.charAt(index);
          }
        catch (StringIndexOutOfBoundsException e) {
          //e.printStackTrace();
          output = 0;
          }
        catch (NullPointerException e){
          mode=0;
          output=0;
        }
        return output;
    }

  int noteLength=8;
void parseAndSend(){
	int soundflag=0;
	char charread;
	int chroma=0;
        int noteSymbol = 0;
	int breakflag=0;
	int dot=0;
	//lineが空だったら1行新しく読み込む
	if(line==null){
		line=fileReadLine(reader);
	}

	while(true){
		//charread=line.charAt(index);
		charread=stringcharReadAt(line,index);
		if(charread==0){
			index=0;
			line=fileReadLine(reader);
			charread=stringcharReadAt(line,index);

			if(charread==0){
				//mode=0;
				index=0;
				println("blank line");
				line=fileReadLine(reader);
				charread=stringcharReadAt(line,index);

				if(charread==0){
				//mode=0;
				index=0;
				mode=0;
				println("song end");
				break;
			}
			}

		}
		switch(charread){

			elif charRead== 'c':
			if(soundflag==0){
					soundflag=1;
					chroma = 3 + (octave-1)*12;
				}
				else{//soundflag==1 既に一度音を読んでいる場合
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;
			elif charRead== 'd':
				if(soundflag==0){
					soundflag=1;
					chroma= 5 + (octave-1)*12;
				}
				else{//soundflag==1 既に一度音を読んでいる場合
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;
			elif charRead== 'e':
				if(soundflag==0){
					soundflag=1;
					chroma= 7 + (octave-1)*12;
				}
				else{//soundflag==1 既に一度音を読んでいる場合
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;
			elif charRead== 'f':
				if(soundflag==0){
					soundflag=1;
					chroma= 8 + (octave-1)*12;
				}
				else{//soundflag==1 既に一度音を読んでいる場合
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;
			elif charRead== 'g':
				if(soundflag==0){
					soundflag=1;
					chroma=10 + (octave-1)*12;
				}
				else{//soundflag==1 既に一度音を読んでいる場合
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;
			elif charRead== 'a':
				if(soundflag==0){
					soundflag=1;
					chroma=0 + (octave)*12;
				}
				else{//soundflag==1 既に一度音を読んでいる場合
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;
			elif charRead== 'b':
				if(soundflag==0){
					soundflag=1;
					chroma=2 + octave*12;
				}
				else{//soundflag==1 既に一度音を読んでいる場合
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;

			elif charRead== 'r':
				if(soundflag==0){
					soundflag=1;
					chroma=-1;
				}
				else{//soundflag==1 既に一度音を読んでいる場合
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;


			elif charRead== 'o':
			elif charRead== 'O':
				if(soundflag==0){
					index++;
					octave = line.charAt(index)-48;
				}
				else{
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;

			elif charRead== '<'://ascii 60
			elif charRead== '>'://ascii 62
				if(soundflag==0){
					octave += charread-61;
				}
				else{
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				break;

			elif charRead== '2':
			elif charRead== '4':
			elif charRead== '8':
				noteSymbol=charread-48;
				break;
			elif charRead== '6':
				noteSymbol=16;
				break;

			elif charRead== '1':
				if(stringcharReadAt(line,++index)=='6'){
					noteSymbol=16;
				}
                                else if(stringcharReadAt(line,index)=='2'){
                                        noteSymbol=12;
                                }
				else{
					index--;
					noteSymbol=1;
				}
				break;
			elif charRead== 'l':
				if(soundflag == 1){
					caliculateNote(chroma,noteSymbol,dot);
					breakflag=1;
				}
				else{
				switch(stringcharReadAt(line,++index)){
					elif charRead== '1':
						if(stringcharReadAt(line,++index)=='6'){
						noteLength=16;
						}
						else{
						index--;
						noteLength=1;
						}
						index--;
						break;
					elif charRead== '2':
						noteLength=2;
						index--;
						break;
					elif charRead== '4':
						noteLength=4;
						index--;
						break;
					elif charRead== '8':
						noteLength=8;
						index--;
						break;
					}
				break;
				}
			elif charRead== '+':
				chroma++;
				break;

			elif charRead== '-':
				chroma--;
				break;

			elif charRead== '.':
				dot = 1;
				break;

			elif charRead== 'S':
				index+=3;
				break;
			elif charRead== '}':
				index+=2;
				break;
		}
		if(breakflag==1){break;}
		index++;
	}
}
"""
