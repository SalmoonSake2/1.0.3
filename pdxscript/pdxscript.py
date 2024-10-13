
import typing
import codecs

class Statement:
    '''
    Description
    -----------------------------------------------------------------------
    Data Storing Class for pdx script statement. Such as scope, effect, and 
    trigger.

    Function
    -----------------------------------------------------------------------
    - `__init__()` : initialize the storing object with given keyword and value.
    - `get_keyword()` : get the keyword of the Statement object.
    - `get_value()` : get the value of the Statement object.
    - `get_operator()` get the operator of the Statement object.
    - `set_keyowrd()` : set the keyword of the Statement object.
    - `set_value()` : set the value of the Statement object.
    - `set_operator()` : set the operator of the Statement object.

    Usage
    -----------------------------------------------------------------------
    >>> statements = []
    >>> characters = ("PYT_cat","PYT_dog","PYT_bird")
    >>> for character in charaters:
    >>>     statements.append(Statement("recruit_character",character))
    >>> print(statements)

    '''

    def __init__(self,keyword:str = None, value:typing.Union[str,list,'PDXscript'] = None, operator:typing.Literal["#E","#G","#S"] = "#E") -> None:
        '''
        Description
        -----------------------------------------------------------------------
        initialize Statement object with given keyword, value, and operator.
        Every PDXscript statement can organize into the form:

        >>> keyword operator value

        for example:
        
        >>> set_country_flag = GER_has_hilt
        >>> is_capitulated = yes
        >>> trigger = {}
        
        you can also create empty Statement by:

        >>> empty_statement = Statement()

        this is useful for some cases.

        Parameters
        -----------------------------------------------------------------------
        - `keyword` (str) : the string wanted to stored as keyword of Statement object.
        - `value` (str | list | PDXscript) : the string wanted to stored as value of the Statement object.
        - `operator` (str) : the operator if the Statement. #E represnts equal, #G
        represents grater, and #S represents smaller

        Return
        -----------------------------------------------------------------------
        There's no return of this method.

        Usage
        -----------------------------------------------------------------------
        >>> flag = "SPR_civil_war_going_on"
        >>> has_global_flag = Statement("has_global_flag",flag)
        '''
        self._keyword = keyword
        self._value = value
        self._operator = operator

    def get_keyword(self) -> str:
        return self._keyword
    
    def get_value(self) -> typing.Union[str,list,'PDXscript'] :
        return self._value
    
    def get_operator(self,literal:bool = False) -> typing.Literal['#E','#G','#S', '=', ">", "<"]:

        '''
        Description
        -----------------------------------------------------------------------
        Get the operator of the Statement object. If set literal parameter to
        True, it'll return the literal signal of the Statement. Default False
        for returning the symbols for equal(#E), greater(#G), or smaller(#S).
        
        Parameters
        -----------------------------------------------------------------------
        - `literal` (bool) : whether to return the literal symbols of operator.

        Returns
        -----------------------------------------------------------------------
        Literal["#E","#G","#S","=",">","<"]

        '''

        if not literal:
            return self._operator
        
        else:
            if self._operator == "#E":
                return "="
            
            elif self._operator == "#G":
                return ">"
            
            elif self._operator == "#S":
                return "<"

    def set_keyowrd(self,keyword:str) -> None:
        self._keyword = keyword

    def set_value(self,value:typing.Union[str,list,'PDXscript']) -> None:
        self._value = value

    def set_operator(self, operator:typing.Literal["#E","#G","#S"]) -> None:
        self._operator = operator
        
class PDXscript:
    '''
    Description
    -----------------------------------------------------------------------
    Data Storing Class for pdx script. Also provide methods to read/write 
    pdx script file. It's actually a list of Statements, so you can use
    `for` to iterate it.

    Function
    -----------------------------------------------------------------------
    - `__init__()` : Initialize the object from given pdx script.
    - `append()` : Add a Statement to the PDXscript object.
    - `insert()` : Insert a Statement to the PDXscript object.
    - `remove()` : Remove a Statement from the PDXscript object.
    - `pop()` : Remove a Statement from PDXscript object by index.
    - `extend()` : Extend PDXscript objects together.
    - `read()` : Read a given pdx script file and return PDXscript object.
    - `write()` : Write the PDXscript object to the file.
    - `_getTextBuffer()` : Internal method. Get the textBuffer from given script.
    - `_getToken()` : Internal method. Get the tokens from given pdx script.
    - `_getStructure()` : Internal method. Get PDXscript object from given token.

    Usage
    -----------------------------------------------------------------------
    >>> path = "C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/common/national_focus/finland.txt"
    >>> script = PDXscript(path)
    >>> script.append(myFocus)
    '''

    def __init__(self,path:str = None,statements:list['Statement'] = None) -> None:
        '''
        Description
        -----------------------------------------------------------------------
        Initialize the object from given pdx script file or list of statement.

        Parameters
        -----------------------------------------------------------------------
        - path (str): The path of the pdx script file.
        - statements (list[Statement]): The Statement objects want to convert to PDXscript.

        Return
        -----------------------------------------------------------------------
        There's no return of this method.

        Raise
        -----------------------------------------------------------------------
        - TokenNotFoundException : if there's an unknown token in the pdx script.
        - ScriptNotClosedException : if the script's bracket isn't closed.

        Usage
        -----------------------------------------------------------------------
        >>> path = "C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/common/national_focus/finland.txt"
        >>> script = PDXscript(path)
        '''

        self._index = 0

        if path == None and statements == None:
            self._element = []
            return
        
        if statements != None:
            self._element = statements
            return

        textBuffer:list[str] = []

        with open(file = path,mode = "r",encoding="utf-8-sig") as sourceFile:
            for line in sourceFile:
                textBuffer.append(line)

        self._element:list['Statement'] = self._getStructure(self._getToken(textBuffer))

        if self._element == -1:
            raise ScriptNotClosedException("The bracket isn't closed in the pdx script file")
        
    def __iter__(self) -> 'PDXscript':
        self._index = 0
        return self
    
    def __next__(self) -> 'Statement':

        if self._index < len(self._element):
            result = self._element[self._index]
            self._index += 1
            return result
        
        else:
            raise StopIteration

    def __getitem__(self,index:int) -> 'Statement':
        return self._element[index]
    
    def __setitem__(self,index:int, value:'Statement') -> None:

        if not isinstance(value, Statement):
            raise TypeError("The __setitem__() method should always has value in Statement class.")
        
        self._element[index] = value

    def __len__(self) -> int:
        return len(self._element)

    def append(self, statement: 'Statement') -> 'PDXscript':

        if not isinstance(statement, Statement):
            raise TypeError("append() method only takes Statement object as argrument")
        
        self._element.append(statement)
        return self._element

    def insert(self, statement: 'Statement', index: int) -> 'PDXscript':

        if not isinstance(statement, Statement):
            raise TypeError("insert() method only takes Statement object as argrument")

        self._element.insert(index, statement)
        return self._element

    def remove(self, arg: 'Statement') -> 'PDXscript':

        if len(self._element) == 0:
            return PDXscript()

        elif isinstance(arg,'Statement'):
            self._element.remove(arg)
            return self._element

        else:
            raise TypeError('remove_statement() only take Statement object as paramenter')

    def pop(self,index:int) -> 'PDXscript':
        self._element.pop(index)
        return self._element

    def extend(self,script:typing.Union['PDXscript',list['PDXscript']]) -> 'PDXscript':

        if issubclass(type(script),'PDXscript'):

            self._element.extend(script)
            return self._element

        elif isinstance(script, list['PDXscript']):

            for pdxscriptObj in script:
                self._element.extend(pdxscriptObj)

            return self._element
        
        raise TypeError("Wrong argument type for combine()")
    
    def read(self, filePath:str) -> 'PDXscript':
        '''
        Description
        -----------------------------------------------------------------------
        Read a given PDXscript file and return the PDXscript object.

        Parameters
        -----------------------------------------------------------------------
        - `filePath` (str): the path of the pdx file.

        Return
        -----------------------------------------------------------------------
        PDXscript : the transformed object.

        Usage
        -----------------------------------------------------------------------
        >>> my_focus = PDXscript().read(path)
        '''

        temp_pdx = PDXscript(filePath)

        return temp_pdx

    def write(self, filePath:str) -> None:
        '''
        Description
        -----------------------------------------------------------------------
        Write the script as PDX script to the path file.
        
        Parameters
        -----------------------------------------------------------------------
        - `filePath` (str) : the path of the file want to write. Couldn't be
        the original path of Heart of Iron IV.

        Return
        -----------------------------------------------------------------------
        There's no return of the method.

        Raise
        -----------------------------------------------------------------------
        ViolatedPathException: When try to write the original game file.

        Usage
        -----------------------------------------------------------------------
        >>> my_focusTree = FocusTree()...
        >>> my_focusTree.write(path)

        '''
        
        invalid_path = "Steam/steamapps/common/Hearts of Iron IV"

        if invalid_path in filePath:
            raise ViolatedPathException("You cannot write any file at this location! Please try another path.")

        textBuffer = []

        textBuffer.append("#This code is generated by Salmoon's generator.")
        textBuffer.extend(self._getTextBuffer(self._element))
        textBuffer.append("#EOF")

        with codecs.open(filePath,"w",'utf-8-sig') as file:
            for line in textBuffer:
                file.write(line + "\n")
        
    def _getTextBuffer(self,statements:list['Statement'],level:int = 0, textBuffer:list = []) -> list[str]:
        '''
        Description
        -----------------------------------------------------------------------
        Internal method. Get textBuffer by Iteration from statements.

        Parameters
        -----------------------------------------------------------------------
        - `statements` (list [ Statement ]) : the statement that want to convert.
        - `level` (int) : the depth of the tree structure.
        - `textBuffer` (list) : the buffer using for iteration.

        Return
        -----------------------------------------------------------------------
        list[str] : the textBuffer

        '''

        for statement in statements:

            if issubclass(type(statement.get_value()), PDXscript) or isinstance(statement.get_value(), list):

                if len(statement.get_value()) == 0:
                    textBuffer.append("\t" * level +
                                      statement.get_keyword() +
                                      " {\n" +
                                      "\t" * level +
                                      "}")
                    continue

                if isinstance(statement.get_value()[0], Statement):
                    textBuffer.append("\t" * level +
                                    statement.get_keyword() +
                                    " " +
                                    statement.get_operator(literal=True)+
                                    " {")
                    self._getTextBuffer(statement.get_value(), level+1, textBuffer)
                
                else:
                    textBuffer.append("\t" * level +
                                  statement.get_keyword() +
                                  " " +
                                  statement.get_operator(literal=True)+
                                  " {")

                    text_list = "\t" * (level + 1) + str(statement.get_value()[0])
                    for obj in statement.get_value()[1:]:
                        text_list = text_list + " " + str(obj)
                
                    textBuffer.append(text_list)
                    textBuffer.append("\t" * level +"}")

            elif isinstance(statement.get_value(), str):
                textBuffer.append("\t" * level + 
                                  statement.get_keyword() + 
                                  " " +
                                  statement.get_operator(literal=True) +
                                  " " +
                                  statement.get_value())
        
        if level != 0:
            textBuffer.append("\t" * (level-1) +"}")

        return textBuffer

    def _getToken(self,textBuffer:list[str]) -> list[str]:
        '''
        Description
        -----------------------------------------------------------------------
        Internal method. Get the tokens string from given pdx script.

        Parameters
        -----------------------------------------------------------------------
        - textBuffer (list[str]): the list of lined script.

        Return
        -----------------------------------------------------------------------
        list[str] : the token string get from the textBuffer.
        '''

        tokens:list[str] = []
        word:str = ""
        
        for line in textBuffer:

            has_quoatation_mark = False
            has_back_slash = False

            for char in line:

                if not char in "\t \n={}><#\"\\" or has_quoatation_mark and not char in "\"\\":
                    word += char
                
                elif char in "\t \n}#" and not has_quoatation_mark:

                    if word:
                        tokens.append(word)
                        word = ""

                    if char == "}":
                        tokens.append("#R")

                    if char == "#":
                        break

                elif char in "=><":

                    if word:
                        tokens.append(word)
                        word = ""

                    token_mapping = {
                        "=" : "#E",
                        ">" : "#G",
                        "<" : "#S"
                    }
                    tokens.append(token_mapping[char])

                elif char == "{":
                    tokens.append("#L")
                
                elif char == "\"":

                    word += char

                    if not has_back_slash:
                        has_quoatation_mark = not has_quoatation_mark
                    else:
                        has_back_slash = False
                
                elif char == "\\":
                    word += char
                    has_back_slash = True
        
        return tokens

    def _getStructure(self,tokens:list[str]) -> 'PDXscript':
        '''
        Description
        -----------------------------------------------------------------------
        Internal method. Get the PDXscript from given token.

        Parameters
        -----------------------------------------------------------------------
        - tokens (list[Token]): the list of tokens.

        Return
        -----------------------------------------------------------------------
        PDXscript : the script from given token.
        '''
        is_statement:bool = False
        temp:list[str] = []
        stack:list['PDXscript'] = []
        current_script:'PDXscript' = PDXscript()

        for token in tokens:
            
            if token in "#E#G#S":
                is_statement = True
                temp.append(token)

            elif token == "#L":
                current_script.append(Statement(temp[0],"",temp[1]))
                stack.append(current_script)
                temp = []
                current_script = PDXscript()
                is_statement = False

            elif token == "#R":
                if current_script:
                    last_script = stack.pop()
                    last_script[-1].set_value(current_script)
                    current_script = last_script

                else:
                    last_script = stack.pop()
                    last_script[-1].set_value(temp)
                    temp = []
                    current_script = last_script
            
            else:

                if is_statement:
                    is_statement = False
                    current_script.append(Statement(temp[0],token,temp[1]))
                    temp = []

                else:
                    temp.append(token)
        
        return current_script

class ScriptNotClosedException(Exception):
    def __init__(self,message) -> None:
        super().__init__(message)

class ViolatedPathException(Exception):
    def __init__(self,message) -> None:
        super().__init__(message)