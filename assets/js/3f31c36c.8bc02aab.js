"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[1953],{3905:function(e,n,t){t.d(n,{Zo:function(){return p},kt:function(){return f}});var o=t(7294);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function i(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);n&&(o=o.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,o)}return t}function r(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?i(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function l(e,n){if(null==e)return{};var t,o,a=function(e,n){if(null==e)return{};var t,o,a={},i=Object.keys(e);for(o=0;o<i.length;o++)t=i[o],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(o=0;o<i.length;o++)t=i[o],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var s=o.createContext({}),c=function(e){var n=o.useContext(s),t=n;return e&&(t="function"==typeof e?e(n):r(r({},n),e)),t},p=function(e){var n=c(e.components);return o.createElement(s.Provider,{value:n},e.children)},d={inlineCode:"code",wrapper:function(e){var n=e.children;return o.createElement(o.Fragment,{},n)}},u=o.forwardRef((function(e,n){var t=e.components,a=e.mdxType,i=e.originalType,s=e.parentName,p=l(e,["components","mdxType","originalType","parentName"]),u=c(t),f=a,m=u["".concat(s,".").concat(f)]||u[f]||d[f]||i;return t?o.createElement(m,r(r({ref:n},p),{},{components:t})):o.createElement(m,r({ref:n},p))}));function f(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var i=t.length,r=new Array(i);r[0]=u;var l={};for(var s in n)hasOwnProperty.call(n,s)&&(l[s]=n[s]);l.originalType=e,l.mdxType="string"==typeof e?e:a,r[1]=l;for(var c=2;c<i;c++)r[c]=t[c];return o.createElement.apply(null,r)}return o.createElement.apply(null,t)}u.displayName="MDXCreateElement"},2595:function(e,n,t){t.r(n),t.d(n,{frontMatter:function(){return l},contentTitle:function(){return s},metadata:function(){return c},toc:function(){return p},default:function(){return u}});var o=t(7462),a=t(3366),i=(t(7294),t(3905)),r=["components"],l={},s="Evolve",c={unversionedId:"advanced_features/Evolve",id:"advanced_features/Evolve",isDocsHomePage:!1,title:"Evolve",description:"spock provides evolve functionality similar to the underlying attrs library",source:"@site/docs/advanced_features/Evolve.md",sourceDirName:"advanced_features",slug:"/advanced_features/Evolve",permalink:"/spock/advanced_features/Evolve",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/advanced_features/Evolve.md",tags:[],version:"current",frontMatter:{},sidebar:"docs",previous:{title:"Utilizing Command Line Overrides",permalink:"/spock/advanced_features/Command-Line-Overrides"},next:{title:"Resolvers",permalink:"/spock/advanced_features/Resolvers"}},p=[{value:"Using Evolve",id:"using-evolve",children:[]},{value:"Maintaining CLI and Python API Configuration Parity",id:"maintaining-cli-and-python-api-configuration-parity",children:[]}],d={toc:p};function u(e){var n=e.components,t=(0,a.Z)(e,r);return(0,i.kt)("wrapper",(0,o.Z)({},d,t,{components:n,mdxType:"MDXLayout"}),(0,i.kt)("h1",{id:"evolve"},"Evolve"),(0,i.kt)("p",null,(0,i.kt)("inlineCode",{parentName:"p"},"spock")," provides evolve functionality similar to the underlying attrs library\n(",(0,i.kt)("a",{parentName:"p",href:"https://www.attrs.org/en/stable/api.html#attrs.evolve"},"attrs.evolve"),". ",(0,i.kt)("inlineCode",{parentName:"p"},"evolve()")," creates a new\n",(0,i.kt)("inlineCode",{parentName:"p"},"Spockspace")," instance based on differences between the underlying declared state and any passed in instantiated\n",(0,i.kt)("inlineCode",{parentName:"p"},"@spock")," decorated classes."),(0,i.kt)("h3",{id:"using-evolve"},"Using Evolve"),(0,i.kt)("p",null,"The ",(0,i.kt)("inlineCode",{parentName:"p"},"evolve()")," method is available form the ",(0,i.kt)("inlineCode",{parentName:"p"},"SpockBuilder")," object. ",(0,i.kt)("inlineCode",{parentName:"p"},"evolve()")," takes as input a variable number of\ninstantiated ",(0,i.kt)("inlineCode",{parentName:"p"},"@spock")," decorated classes, evolves the underlying ",(0,i.kt)("inlineCode",{parentName:"p"},"attrs")," objects to incorporate the changes between\nthe instantiated classes and the underlying classes, and returns the new ",(0,i.kt)("inlineCode",{parentName:"p"},"Spockspace")," object."),(0,i.kt)("p",null,"For instance:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"\nfrom enum import Enum\nfrom spock import spock\nfrom spock import SpockBuilder\n\n\nclass Choices(Enum):\n    choice1 = 1\n    choice2 = 2\n\n\n@spock\nclass Configs4OneThing:\n    the_choice: Choices = Choices.choice1\n    param: int = 10\n\n\ndef main():\n    evolve_class = Configs4OneThing(param=20)\n    evolved_configs = SpockBuilder(Configs4OneThing, desc='Evolve Example').evolve(evolve_class)\n    print(evolved_configs)\n    \nif __name__ == '__main__':\n    main()\n")),(0,i.kt)("p",null,"This would evolve the value of ",(0,i.kt)("inlineCode",{parentName:"p"},"param")," to be 20 instead of the default value of 10. The print output would be:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-shell"},"Configs4OneThing: !!python/object:spock.backend.config.Configs4OneThing\n  param: 20\n  the_choice: 1\n")),(0,i.kt)("h3",{id:"maintaining-cli-and-python-api-configuration-parity"},"Maintaining CLI and Python API Configuration Parity"),(0,i.kt)("p",null,(0,i.kt)("inlineCode",{parentName:"p"},"evolve")," is quite useful when writing python code/libraries/packages that maintain both a CLI and a Python API. With\n",(0,i.kt)("inlineCode",{parentName:"p"},"spock")," it is simple to maintain parity between the CLI and the Python API by leveraging the ",(0,i.kt)("inlineCode",{parentName:"p"},"evolve")," functionality."),(0,i.kt)("p",null,"For instance, let's say we have two different ",(0,i.kt)("inlineCode",{parentName:"p"},"@spock")," decorated configs we want to use for both the CLI and the Python\nAPI:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"# config.py\n\nfrom enum import Enum\nfrom spock import spock\nfrom typing import List\n\n\nclass Choices(Enum):\n    choice1 = 1\n    choice2 = 2\n\n\n@spock\nclass Configs4OneThing:\n    the_choice: Choices = Choices.choice1\n    param: int = 10\n\n\n@spock\nclass Configs4AnotherThing:\n    some_list: List[float] = [10.0, 20.0]\n    flag: bool = False\n\n    \n# List of all configs\nALL_CONFIGS = [\n    Configs4OneThing,\n    Configs4AnotherThing\n]\n\n")),(0,i.kt)("p",null,"With these ",(0,i.kt)("inlineCode",{parentName:"p"},"@spock")," decorated classes it's easy to write a parent class that contains shared functionality (i.e. run a\nmodel, do some work, etc.) and two child classes that handle the slightly different syntax needed for the underlying\n",(0,i.kt)("inlineCode",{parentName:"p"},"SpockBuilder")," for the CLI and for the Python API. "),(0,i.kt)("p",null,"For the CLI, we use the common ",(0,i.kt)("inlineCode",{parentName:"p"},"spock")," syntax that has been shown in previous examples/tutorial. Call the builder\nobject and pass in all ",(0,i.kt)("inlineCode",{parentName:"p"},"@spock")," decorated classes. Keep the ",(0,i.kt)("inlineCode",{parentName:"p"},"no_cmd_line")," flag set to ",(0,i.kt)("inlineCode",{parentName:"p"},"False")," which will automatically\ngenerate a command line argument for each defined parameter and provide support for the ",(0,i.kt)("inlineCode",{parentName:"p"},"--config")," argument to pass\nin values via a markdown file(s). We then call ",(0,i.kt)("inlineCode",{parentName:"p"},"generate")," on the builder to return the ",(0,i.kt)("inlineCode",{parentName:"p"},"Spockspace"),"."),(0,i.kt)("p",null,"For the Python API, we modify the ",(0,i.kt)("inlineCode",{parentName:"p"},"spock")," syntax slightly. We still pass in all ",(0,i.kt)("inlineCode",{parentName:"p"},"@spock")," decorated classes but set\nthe ",(0,i.kt)("inlineCode",{parentName:"p"},"no_cmd_line")," flag to ",(0,i.kt)("inlineCode",{parentName:"p"},"True")," to prevent command line arguments (and markdown configuration). We then call ",(0,i.kt)("inlineCode",{parentName:"p"},"evolve"),"\nand pass in any user instantiated ",(0,i.kt)("inlineCode",{parentName:"p"},"@spock")," decorated classes to evolve the underlying object and return a new\n",(0,i.kt)("inlineCode",{parentName:"p"},"Spockspace")," object that has been evolved based on the differences between the values within instantiated classes and\nthe values in the underlying object."),(0,i.kt)("p",null,"Example code is given below:"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},'# code.py\nfrom abc import ABC\nfrom spock import SpockBuilder\nfrom config import ALL_CONFIGS\n\n\nclass Base(ABC):\n    def run(self):\n        # do something with self.configs\n        ...\n\n    \nclass OurAPI(Base):\n    def __init__(self,\n                 config_4_one_thing: Configs4OneThing = Configs4OneThing(), \n                 config_4_another_thing: Configs4AnotherThing = Configs4AnotherThing()\n                 ):\n        # Call the SpockBuilder with the no_cmd_line flag set to True \n        # This will prevent command-line arguments from being generated\n        # Additionally call evolve on the builder with the custom/default Configs4OneThing & Configs4AnotherThing\n        # objects\n        self.configs = SpockBuilder(*ALL_CONFIGS, no_cmd_line=True, configs=[]).evolve(\n            config_4_one_thing, config_4_another_thing\n        )\n\n\nclass OurCLI(Base):\n    def __init__(self):\n        # Call the SpockBuilder with the no_cmd_line flag set to False (default value)\n        # This will automatically provide command-line arguments for all of the @spock decorated\n        # config classes\n        self.configs = SpockBuilder(*ALL_CONFIGS).generate()\n    \n\ndef cli_shim():\n    """Shim function for setup.py entry_points\n\n    Returns:\n        None\n    """\n    cli_runner = OurCLI().run()\n')))}u.isMDXComponent=!0}}]);