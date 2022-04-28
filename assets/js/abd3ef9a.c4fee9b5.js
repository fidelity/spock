"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[9311],{3905:function(e,t,r){r.d(t,{Zo:function(){return l},kt:function(){return k}});var n=r(7294);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function c(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function a(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?c(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):c(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function p(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},c=Object.keys(e);for(n=0;n<c.length;n++)r=c[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var c=Object.getOwnPropertySymbols(e);for(n=0;n<c.length;n++)r=c[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}var s=n.createContext({}),i=function(e){var t=n.useContext(s),r=t;return e&&(r="function"==typeof e?e(t):a(a({},t),e)),r},l=function(e){var t=i(e.components);return n.createElement(s.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var r=e.components,o=e.mdxType,c=e.originalType,s=e.parentName,l=p(e,["components","mdxType","originalType","parentName"]),d=i(r),k=o,f=d["".concat(s,".").concat(k)]||d[k]||u[k]||c;return r?n.createElement(f,a(a({ref:t},l),{},{components:r})):n.createElement(f,a({ref:t},l))}));function k(e,t){var r=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var c=r.length,a=new Array(c);a[0]=d;var p={};for(var s in t)hasOwnProperty.call(t,s)&&(p[s]=t[s]);p.originalType=e,p.mdxType="string"==typeof e?e:o,a[1]=p;for(var i=2;i<c;i++)a[i]=r[i];return n.createElement.apply(null,a)}return n.createElement.apply(null,r)}d.displayName="MDXCreateElement"},9715:function(e,t,r){r.r(t),r.d(t,{frontMatter:function(){return p},contentTitle:function(){return s},metadata:function(){return i},toc:function(){return l},default:function(){return d}});var n=r(7462),o=r(3366),c=(r(7294),r(3905)),a=["components"],p={sidebar_label:"exceptions",title:"exceptions"},s=void 0,i={unversionedId:"reference/exceptions",id:"reference/exceptions",isDocsHomePage:!1,title:"exceptions",description:"\\_SpockUndecoratedClass Objects",source:"@site/docs/reference/exceptions.md",sourceDirName:"reference",slug:"/reference/exceptions",permalink:"/spock/reference/exceptions",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/reference/exceptions.md",tags:[],version:"current",frontMatter:{sidebar_label:"exceptions",title:"exceptions"},sidebar:"api",previous:{title:"builder",permalink:"/spock/reference/builder"},next:{title:"graph",permalink:"/spock/reference/graph"}},l=[{value:"_SpockUndecoratedClass Objects",id:"_spockundecoratedclass-objects",children:[]},{value:"_SpockInstantiationError Objects",id:"_spockinstantiationerror-objects",children:[]},{value:"_SpockNotOptionalError Objects",id:"_spocknotoptionalerror-objects",children:[]},{value:"_SpockDuplicateArgumentError Objects",id:"_spockduplicateargumenterror-objects",children:[]},{value:"_SpockEvolveError Objects",id:"_spockevolveerror-objects",children:[]},{value:"_SpockValueError Objects",id:"_spockvalueerror-objects",children:[]}],u={toc:l};function d(e){var t=e.components,r=(0,o.Z)(e,a);return(0,c.kt)("wrapper",(0,n.Z)({},u,r,{components:t,mdxType:"MDXLayout"}),(0,c.kt)("h2",{id:"_spockundecoratedclass-objects"},"_","SpockUndecoratedClass Objects"),(0,c.kt)("pre",null,(0,c.kt)("code",{parentName:"pre",className:"language-python"},"class _SpockUndecoratedClass(Exception)\n")),(0,c.kt)("p",null,"Custom exception type for non spock decorated classes and not dynamic"),(0,c.kt)("h2",{id:"_spockinstantiationerror-objects"},"_","SpockInstantiationError Objects"),(0,c.kt)("pre",null,(0,c.kt)("code",{parentName:"pre",className:"language-python"},"class _SpockInstantiationError(Exception)\n")),(0,c.kt)("p",null,"Custom exception for when the spock class cannot be instantiated correctly"),(0,c.kt)("h2",{id:"_spocknotoptionalerror-objects"},"_","SpockNotOptionalError Objects"),(0,c.kt)("pre",null,(0,c.kt)("code",{parentName:"pre",className:"language-python"},"class _SpockNotOptionalError(Exception)\n")),(0,c.kt)("p",null,"Custom exception for missing value"),(0,c.kt)("h2",{id:"_spockduplicateargumenterror-objects"},"_","SpockDuplicateArgumentError Objects"),(0,c.kt)("pre",null,(0,c.kt)("code",{parentName:"pre",className:"language-python"},"class _SpockDuplicateArgumentError(Exception)\n")),(0,c.kt)("p",null,"Custom exception type for duplicated values"),(0,c.kt)("h2",{id:"_spockevolveerror-objects"},"_","SpockEvolveError Objects"),(0,c.kt)("pre",null,(0,c.kt)("code",{parentName:"pre",className:"language-python"},"class _SpockEvolveError(Exception)\n")),(0,c.kt)("p",null,"Custom exception for when evolve errors occur"),(0,c.kt)("h2",{id:"_spockvalueerror-objects"},"_","SpockValueError Objects"),(0,c.kt)("pre",null,(0,c.kt)("code",{parentName:"pre",className:"language-python"},"class _SpockValueError(Exception)\n")),(0,c.kt)("p",null,"Custom exception for throwing value errors"))}d.isMDXComponent=!0}}]);