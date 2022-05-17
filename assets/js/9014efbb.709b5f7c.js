"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[5289],{3905:function(e,r,t){t.d(r,{Zo:function(){return s},kt:function(){return f}});var n=t(7294);function a(e,r,t){return r in e?Object.defineProperty(e,r,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[r]=t,e}function p(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function c(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?p(Object(t),!0).forEach((function(r){a(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):p(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}function o(e,r){if(null==e)return{};var t,n,a=function(e,r){if(null==e)return{};var t,n,a={},p=Object.keys(e);for(n=0;n<p.length;n++)t=p[n],r.indexOf(t)>=0||(a[t]=e[t]);return a}(e,r);if(Object.getOwnPropertySymbols){var p=Object.getOwnPropertySymbols(e);for(n=0;n<p.length;n++)t=p[n],r.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var i=n.createContext({}),l=function(e){var r=n.useContext(i),t=r;return e&&(t="function"==typeof e?e(r):c(c({},r),e)),t},s=function(e){var r=l(e.components);return n.createElement(i.Provider,{value:r},e.children)},u={inlineCode:"code",wrapper:function(e){var r=e.children;return n.createElement(n.Fragment,{},r)}},d=n.forwardRef((function(e,r){var t=e.components,a=e.mdxType,p=e.originalType,i=e.parentName,s=o(e,["components","mdxType","originalType","parentName"]),d=l(t),f=a,m=d["".concat(i,".").concat(f)]||d[f]||u[f]||p;return t?n.createElement(m,c(c({ref:r},s),{},{components:t})):n.createElement(m,c({ref:r},s))}));function f(e,r){var t=arguments,a=r&&r.mdxType;if("string"==typeof e||a){var p=t.length,c=new Array(p);c[0]=d;var o={};for(var i in r)hasOwnProperty.call(r,i)&&(o[i]=r[i]);o.originalType=e,o.mdxType="string"==typeof e?e:a,c[1]=o;for(var l=2;l<p;l++)c[l]=t[l];return n.createElement.apply(null,c)}return n.createElement.apply(null,t)}d.displayName="MDXCreateElement"},1233:function(e,r,t){t.r(r),t.d(r,{frontMatter:function(){return o},contentTitle:function(){return i},metadata:function(){return l},toc:function(){return s},default:function(){return d}});var n=t(7462),a=t(3366),p=(t(7294),t(3905)),c=["components"],o={sidebar_label:"wrappers",title:"backend.wrappers"},i=void 0,l={unversionedId:"reference/backend/wrappers",id:"reference/backend/wrappers",isDocsHomePage:!1,title:"backend.wrappers",description:"Handles Spock data type wrappers",source:"@site/docs/reference/backend/wrappers.md",sourceDirName:"reference/backend",slug:"/reference/backend/wrappers",permalink:"/spock/reference/backend/wrappers",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/reference/backend/wrappers.md",tags:[],version:"current",frontMatter:{sidebar_label:"wrappers",title:"backend.wrappers"},sidebar:"api",previous:{title:"utils",permalink:"/spock/reference/backend/utils"},next:{title:"builder",permalink:"/spock/reference/builder"}},s=[{value:"Spockspace Objects",id:"spockspace-objects",children:[]}],u={toc:s};function d(e){var r=e.components,t=(0,a.Z)(e,c);return(0,p.kt)("wrapper",(0,n.Z)({},u,t,{components:r,mdxType:"MDXLayout"}),(0,p.kt)("p",null,"Handles Spock data type wrappers"),(0,p.kt)("h2",{id:"spockspace-objects"},"Spockspace Objects"),(0,p.kt)("pre",null,(0,p.kt)("code",{parentName:"pre",className:"language-python"},"class Spockspace(argparse.Namespace)\n")),(0,p.kt)("p",null,"Inherits from Namespace to implement a pretty print on the obj"),(0,p.kt)("p",null,"Overwrites the ",(0,p.kt)("strong",{parentName:"p"},"repr")," method with a pretty version of printing"),(0,p.kt)("h4",{id:"__repr_dict__"},"_","_","repr","_","dict","_","_"),(0,p.kt)("pre",null,(0,p.kt)("code",{parentName:"pre",className:"language-python"},"@property\ndef __repr_dict__()\n")),(0,p.kt)("p",null,"Handles making a clean dict to hind the salt and key on print"),(0,p.kt)("h4",{id:"__repr__"},"_","_","repr","_","_"),(0,p.kt)("pre",null,(0,p.kt)("code",{parentName:"pre",className:"language-python"},"def __repr__()\n")),(0,p.kt)("p",null,"Overloaded repr to pretty print the spock object"),(0,p.kt)("h4",{id:"__iter__"},"_","_","iter","_","_"),(0,p.kt)("pre",null,(0,p.kt)("code",{parentName:"pre",className:"language-python"},"def __iter__()\n")),(0,p.kt)("p",null,"Iter for the underlying dictionary"))}d.isMDXComponent=!0}}]);