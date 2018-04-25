import base64
import logging

LOGGER = logging.getLogger("to_word")

def intToword(number):
    return base64.b64decode(format(number, 'x').decode('hex'))

def writeWordsFile(numberFile, wf):
    wf = open(wf, "w")

    with open(numberFile, "r") as f:
        wordCount = 0
        for number in f:
            num = int(number)
            toword = intToword(num)
            LOGGER.debug("int:%d converted_word:%s", num, toword)
            wf.write("{}\n".format(toword))
            wordCount += 1
        LOGGER.info("Total words in file:%d", wordCount)
    wf.close()

def main():
    LOGGER.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    LOGGER.addHandler(ch)

    writeWordsFile("numbers.txt", "words.txt")

if __name__ == '__main__':
    main()