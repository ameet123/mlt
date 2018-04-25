import base64
import logging

unwantedChars = ['\'', '"', ',', ';', ':', '.']
LOGGER = logging.getLogger("to_number")

def cleanseLine(chars, oneLine):
    for ch in chars:
        oneLine = oneLine.replace(ch, '')
    return oneLine.lower()


def wordToint(word):
    """
    base64 encode the word, then encode it to hexadecimal and then using int builtin, convert to integer 16 digits.
    :param word:
    :return: 16 digit integer
    """
    return int(base64.b64encode(word).encode('hex'), 16)


def intToword(number):
    return base64.b64decode(format(number, 'x').decode('hex'))


def writeNumbersFile(wordFile, nf):
    nf = open(nf, "w")

    with open(wordFile, "r") as f:
        wordCount = 0
        i = 1
        for line in f:
            lineCount = 0
            line = cleanseLine(unwantedChars, line)
            for w in line.split():
                lineCount += 1
                toint = wordToint(w)
                nf.write("{}\n".format(toint))
                toword = intToword(toint)
                LOGGER.debug("base:%s int:%d rev_base:%s strings equal?%s", w, toint, toword, toword == w)
            LOGGER.info("[%d] words:%d=>%s", i, lineCount, line)
            wordCount += lineCount
        LOGGER.info("Total words in file:%d", wordCount)

    nf.close()


def main():
    LOGGER.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    LOGGER.addHandler(ch)

    writeNumbersFile("words-to-numbers.txt", "numbers.txt")


if __name__ == '__main__':
    main()
