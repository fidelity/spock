"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[1890],{3905:function(e,n,t){t.d(n,{Zo:function(){return s},kt:function(){return d}});var r=t(7294);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function i(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function l(e,n){if(null==e)return{};var t,r,a=function(e,n){if(null==e)return{};var t,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var p=r.createContext({}),c=function(e){var n=r.useContext(p),t=n;return e&&(t="function"==typeof e?e(n):i(i({},n),e)),t},s=function(e){var n=c(e.components);return r.createElement(p.Provider,{value:n},e.children)},m={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},u=r.forwardRef((function(e,n){var t=e.components,a=e.mdxType,o=e.originalType,p=e.parentName,s=l(e,["components","mdxType","originalType","parentName"]),u=c(t),d=a,f=u["".concat(p,".").concat(d)]||u[d]||m[d]||o;return t?r.createElement(f,i(i({ref:n},s),{},{components:t})):r.createElement(f,i({ref:n},s))}));function d(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var o=t.length,i=new Array(o);i[0]=u;var l={};for(var p in n)hasOwnProperty.call(n,p)&&(l[p]=n[p]);l.originalType=e,l.mdxType="string"==typeof e?e:a,i[1]=l;for(var c=2;c<o;c++)i[c]=t[c];return r.createElement.apply(null,i)}return r.createElement.apply(null,t)}u.displayName="MDXCreateElement"},3998:function(e,n,t){t.r(n),t.d(n,{frontMatter:function(){return l},contentTitle:function(){return p},metadata:function(){return c},toc:function(){return s},default:function(){return u}});var r=t(7462),a=t(3366),o=(t(7294),t(3905)),i=["components"],l={},p="Drop In Replacement For Argparser",c={unversionedId:"ArgParser-Replacement",id:"ArgParser-Replacement",isDocsHomePage:!1,title:"Drop In Replacement For Argparser",description:"spock can easily be used as a drop in for argparser. This means that all parameter definitions as required to come in",source:"@site/docs/ArgParser-Replacement.md",sourceDirName:".",slug:"/ArgParser-Replacement",permalink:"/spock/ArgParser-Replacement",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/ArgParser-Replacement.md",tags:[],version:"current",frontMatter:{},sidebar:"docs",previous:{title:"Quick Start",permalink:"/spock/Quick-Start"},next:{title:"The Basics of Spock",permalink:"/spock/basics/About"}},s=[{value:"Automatic Command-Line Argument Generation",id:"automatic-command-line-argument-generation",children:[]},{value:"Use Spock via the Command-Line",id:"use-spock-via-the-command-line",children:[]}],m={toc:s};function u(e){var n=e.components,t=(0,a.Z)(e,i);return(0,o.kt)("wrapper",(0,r.Z)({},m,t,{components:n,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"drop-in-replacement-for-argparser"},"Drop In Replacement For Argparser"),(0,o.kt)("p",null,(0,o.kt)("inlineCode",{parentName:"p"},"spock")," can easily be used as a drop in for argparser. This means that all parameter definitions as required to come in\nfrom the command line or from setting defaults within the ",(0,o.kt)("inlineCode",{parentName:"p"},"@spock")," decorated classes."),(0,o.kt)("h3",{id:"automatic-command-line-argument-generation"},"Automatic Command-Line Argument Generation"),(0,o.kt)("p",null,(0,o.kt)("inlineCode",{parentName:"p"},"spock")," will automatically generate command line arguments for each parameter, unless the ",(0,o.kt)("inlineCode",{parentName:"p"},"no_cmd_line=True")," flag is\npassed to the ",(0,o.kt)("inlineCode",{parentName:"p"},"SpockBuilder"),". Let's create a simple example to demonstrate:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"from spock import spock\nfrom typing import Optional\n\n@spock\nclass ExampleConfig:\n    read_path: str = '/tmp'\n    date: int\n    cache_path: Optional[str]\n")),(0,o.kt)("p",null,"Given these definitions, ",(0,o.kt)("inlineCode",{parentName:"p"},"spock")," will automatically generate a command-line argument (via an internally maintained\nargparser) for each parameter within each ",(0,o.kt)("inlineCode",{parentName:"p"},"@spock")," decorated class. The syntax follows simple dot notation\nof ",(0,o.kt)("inlineCode",{parentName:"p"},"--classname.parameter"),". Thus, for our sample classes above, ",(0,o.kt)("inlineCode",{parentName:"p"},"spock")," will automatically generate the following\nvalid command-line arguments:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-shell"},"--ExampleConfig.read_path *value*\n--ExampleConfig.date *value*\n--ExampleConfig.cache_path *value*\n")),(0,o.kt)("h3",{id:"use-spock-via-the-command-line"},"Use Spock via the Command-Line"),(0,o.kt)("p",null,"Simply do not pass a ",(0,o.kt)("inlineCode",{parentName:"p"},"-c")," or ",(0,o.kt)("inlineCode",{parentName:"p"},"--config")," argument at the command line and instead pass in all values to the\nautomatically generated cmd-line arguments."),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-shell"},"python simple.py --ExampleConfig.read_path /my/file/path --ExampleConfig.date 1292838124 \\\n--ExampleConfig.cache_path /path/to/cache/dir\n")))}u.isMDXComponent=!0}}]);