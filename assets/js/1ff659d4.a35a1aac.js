"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[5553],{3905:function(e,t,n){n.d(t,{Zo:function(){return c},kt:function(){return d}});var r=n(7294);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function a(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=r.createContext({}),p=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):a(a({},t),e)),n},c=function(e){var t=p(e.components);return r.createElement(s.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},m=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,i=e.originalType,s=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),m=p(n),d=o,f=m["".concat(s,".").concat(d)]||m[d]||u[d]||i;return n?r.createElement(f,a(a({ref:t},c),{},{components:n})):r.createElement(f,a({ref:t},c))}));function d(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var i=n.length,a=new Array(i);a[0]=m;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l.mdxType="string"==typeof e?e:o,a[1]=l;for(var p=2;p<i;p++)a[p]=n[p];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}m.displayName="MDXCreateElement"},7784:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return l},contentTitle:function(){return s},metadata:function(){return p},toc:function(){return c},default:function(){return m}});var r=n(7462),o=n(3366),i=(n(7294),n(3905)),a=["components"],l={},s="Installation",p={unversionedId:"Installation",id:"Installation",isDocsHomePage:!1,title:"Installation",description:"Requirements",source:"@site/docs/Installation.md",sourceDirName:".",slug:"/Installation",permalink:"/spock/Installation",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/Installation.md",tags:[],version:"current",frontMatter:{},sidebar:"docs",previous:{title:"Home",permalink:"/spock/"},next:{title:"Quick Start",permalink:"/spock/Quick-Start"}},c=[{value:"Requirements",id:"requirements",children:[]},{value:"Install/Upgrade",id:"installupgrade",children:[]}],u={toc:c};function m(e){var t=e.components,n=(0,o.Z)(e,a);return(0,i.kt)("wrapper",(0,r.Z)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("h1",{id:"installation"},"Installation"),(0,i.kt)("h3",{id:"requirements"},"Requirements"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},"Python: 3.6+ (",(0,i.kt)("inlineCode",{parentName:"li"},"[tune]")," extension requires 3.7+)"),(0,i.kt)("li",{parentName:"ul"},"Base Dependencies: attrs, GitPython, PyYAML, toml"),(0,i.kt)("li",{parentName:"ul"},"Tested OS: Ubuntu (16.04, 18.04), OSX (10.14.6, 11.3.1)")),(0,i.kt)("h3",{id:"installupgrade"},"Install/Upgrade"),(0,i.kt)("h4",{id:"pypi"},"PyPi"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-shell"},"pip install spock-config\n")),(0,i.kt)("h4",{id:"w-s3-extension"},"w/ S3 Extension"),(0,i.kt)("p",null,"Extra Dependencies: boto3, botocore, hurry.filesize, s3transfer"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-shell"},"pip install spock-config[s3]\n")),(0,i.kt)("h4",{id:"w-hyper-parameter-tuner-extension"},"w/ Hyper-Parameter Tuner Extension"),(0,i.kt)("p",null,"Requires Python 3.7+"),(0,i.kt)("p",null,"Extra Dependencies: optuna, ax-platform, torch, torchvision, mypy_extensions (Python < 3.8)"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-shell"},"pip install spock-config[tune]\n")),(0,i.kt)("h4",{id:"pip-from-source"},"Pip From Source"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-shell"},"pip install git+https://github.com/fidelity/spock\n")),(0,i.kt)("h4",{id:"build-from-source"},"Build From Source"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-shell"},"git clone https://github.com/fidelity/spock\ncd spock\npip install setuptools wheel\npython setup.py bdist_wheel\npip install /dist/spock-config-X.X.XxX-py3-none-any.whl\n")))}m.isMDXComponent=!0}}]);