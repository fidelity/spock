"use strict";(self.webpackChunkdocs_v_2=self.webpackChunkdocs_v_2||[]).push([[1888],{3905:function(e,t,a){a.d(t,{Zo:function(){return u},kt:function(){return k}});var n=a(7294);function l(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function i(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function r(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?i(Object(a),!0).forEach((function(t){l(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):i(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function p(e,t){if(null==e)return{};var a,n,l=function(e,t){if(null==e)return{};var a,n,l={},i=Object.keys(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)>=0||(l[a]=e[a]);return l}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(l[a]=e[a])}return l}var s=n.createContext({}),o=function(e){var t=n.useContext(s),a=t;return e&&(a="function"==typeof e?e(t):r(r({},t),e)),a},u=function(e){var t=o(e.components);return n.createElement(s.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var a=e.components,l=e.mdxType,i=e.originalType,s=e.parentName,u=p(e,["components","mdxType","originalType","parentName"]),d=o(a),k=l,m=d["".concat(s,".").concat(k)]||d[k]||c[k]||i;return a?n.createElement(m,r(r({ref:t},u),{},{components:a})):n.createElement(m,r({ref:t},u))}));function k(e,t){var a=arguments,l=t&&t.mdxType;if("string"==typeof e||l){var i=a.length,r=new Array(i);r[0]=d;var p={};for(var s in t)hasOwnProperty.call(t,s)&&(p[s]=t[s]);p.originalType=e,p.mdxType="string"==typeof e?e:l,r[1]=p;for(var o=2;o<i;o++)r[o]=a[o];return n.createElement.apply(null,r)}return n.createElement.apply(null,a)}d.displayName="MDXCreateElement"},4163:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return p},contentTitle:function(){return s},metadata:function(){return o},toc:function(){return u},default:function(){return d}});var n=a(7462),l=a(3366),i=(a(7294),a(3905)),r=["components"],p={sidebar_label:"field_handlers",title:"backend.field_handlers"},s=void 0,o={unversionedId:"reference/backend/field_handlers",id:"reference/backend/field_handlers",isDocsHomePage:!1,title:"backend.field_handlers",description:"Handles registering field attributes for spock classes -- deals with the recursive nature of dependencies",source:"@site/docs/reference/backend/field_handlers.md",sourceDirName:"reference/backend",slug:"/reference/backend/field_handlers",permalink:"/spock/reference/backend/field_handlers",editUrl:"https://github.com/fidelity/spock/edit/master/website/docs/reference/backend/field_handlers.md",tags:[],version:"current",frontMatter:{sidebar_label:"field_handlers",title:"backend.field_handlers"},sidebar:"api",previous:{title:"config",permalink:"/spock/reference/backend/config"},next:{title:"handler",permalink:"/spock/reference/backend/handler"}},u=[{value:"RegisterFieldTemplate Objects",id:"registerfieldtemplate-objects",children:[]},{value:"RegisterList Objects",id:"registerlist-objects",children:[]},{value:"RegisterEnum Objects",id:"registerenum-objects",children:[]},{value:"RegisterCallableField Objects",id:"registercallablefield-objects",children:[]},{value:"RegisterGenericAliasCallableField Objects",id:"registergenericaliascallablefield-objects",children:[]},{value:"RegisterSimpleField Objects",id:"registersimplefield-objects",children:[]},{value:"RegisterTuneCls Objects",id:"registertunecls-objects",children:[]},{value:"RegisterSpockCls Objects",id:"registerspockcls-objects",children:[]}],c={toc:u};function d(e){var t=e.components,a=(0,l.Z)(e,r);return(0,i.kt)("wrapper",(0,n.Z)({},c,a,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("p",null,"Handles registering field attributes for spock classes -- deals with the recursive nature of dependencies"),(0,i.kt)("h2",{id:"registerfieldtemplate-objects"},"RegisterFieldTemplate Objects"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class RegisterFieldTemplate(ABC)\n")),(0,i.kt)("p",null,"Base class for handing different field types"),(0,i.kt)("p",null,"Once the configuration dictionary has been assembled from the config file and the command line then we need to\nmap these values to the correct spock classes -- seeing as different types need to be handled differently and\nrecursive calls might be needed (when referencing other spock classes) classes derived from RegisterFieldTemplate\nhandle the logic for making sure the argument dictionary passes to the instantiation of each spock class is\ncorrect"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"special_keys")," - dictionary to check special keys")),(0,i.kt)("h4",{id:"__init__"},"_","_","init","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Init call for RegisterFieldTemplate class"),(0,i.kt)("h4",{id:"__call__"},"_","_","call","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __call__(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Call method for RegisterFieldTemplate"),(0,i.kt)("p",null,"Handles calling the correct method for the type of the attribute"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"_is_attribute_in_config_arguments"},"_","is","_","attribute","_","in","_","config","_","arguments"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def _is_attribute_in_config_arguments(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Checks if an attribute is in the configuration file or keyword arguments dictionary"),(0,i.kt)("p",null,"Will recurse spock classes as dependencies might be defined in the configs class"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - map of the read/cmd-line parameter dictionary to general or class level arguments")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Returns"),":"),(0,i.kt)("p",null,"  boolean if in dictionary"),(0,i.kt)("h4",{id:"_is_attribute_optional"},"_","is","_","attribute","_","optional"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"@staticmethod\ndef _is_attribute_optional(attribute: Type[Attribute])\n")),(0,i.kt)("p",null,"Checks if an attribute is allowed to be optional"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attribute")," - current attribute class")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Returns"),":"),(0,i.kt)("p",null,"  boolean if the optional state is allowed"),(0,i.kt)("h4",{id:"handle_optional_attribute_value"},"handle","_","optional","_","attribute","_","value"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles setting an optional value with its default"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h2",{id:"registerlist-objects"},"RegisterList Objects"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class RegisterList(RegisterFieldTemplate)\n")),(0,i.kt)("p",null,"Class that registers list types"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"special_keys")," - dictionary to check special keys")),(0,i.kt)("h4",{id:"__init__-1"},"_","_","init","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Init call to RegisterList"),(0,i.kt)("h4",{id:"handle_attribute_from_config"},"handle","_","attribute","_","from","_","config"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles a list of spock config classes (aka repeated classes)"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_type"},"handle","_","optional","_","attribute","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles a list of spock config classes (aka repeated classes) if it is optional"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_value-1"},"handle","_","optional","_","attribute","_","value"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles setting the value for an optional basic attribute"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"_process_list"},"_","process","_","list"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"@staticmethod\ndef _process_list(spock_cls, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Rolls up repeated classes into the expected list format"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"spock_cls")," - current spock class"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Returns"),":"),(0,i.kt)("p",null,"  list of rolled up repeated spock classes"),(0,i.kt)("h2",{id:"registerenum-objects"},"RegisterEnum Objects"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class RegisterEnum(RegisterFieldTemplate)\n")),(0,i.kt)("p",null,"Class that registers enum types"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"special_keys")," - dictionary to check special keys")),(0,i.kt)("h4",{id:"__init__-2"},"_","_","init","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Init call to RegisterEnum"),(0,i.kt)("h4",{id:"handle_attribute_from_config-1"},"handle","_","attribute","_","from","_","config"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles getting the attribute set value when the Enum is made up of spock classes"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_type-1"},"handle","_","optional","_","attribute","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles falling back on the optional default for a type based attribute"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_value-2"},"handle","_","optional","_","attribute","_","value"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles setting an optional value with its default"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"_handle_and_register_enum"},"_","handle","_","and","_","register","_","enum"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def _handle_and_register_enum(enum_cls, attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Recurses the enum in case there are nested type definitions"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"enum_cls")," - current enum class"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h2",{id:"registercallablefield-objects"},"RegisterCallableField Objects"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class RegisterCallableField(RegisterFieldTemplate)\n")),(0,i.kt)("p",null,"Class that registers callable types"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"special_keys")," - dictionary to check special keys")),(0,i.kt)("h4",{id:"__init__-3"},"_","_","init","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Init call to RegisterSimpleField"),(0,i.kt)("h4",{id:"handle_attribute_from_config-2"},"handle","_","attribute","_","from","_","config"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles setting a simple attribute when it is a spock class type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_type-2"},"handle","_","optional","_","attribute","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Not implemented for this type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Raises"),":"),(0,i.kt)("p",null,"  _SpockNotOptionalError"),(0,i.kt)("h2",{id:"registergenericaliascallablefield-objects"},"RegisterGenericAliasCallableField Objects"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class RegisterGenericAliasCallableField(RegisterFieldTemplate)\n")),(0,i.kt)("p",null,"Class that registers Dicts containing callable types"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"special_keys")," - dictionary to check special keys")),(0,i.kt)("h4",{id:"__init__-4"},"_","_","init","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Init call to RegisterSimpleField"),(0,i.kt)("h4",{id:"handle_attribute_from_config-3"},"handle","_","attribute","_","from","_","config"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles setting a simple attribute when it is a spock class type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_type-3"},"handle","_","optional","_","attribute","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Not implemented for this type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Raises"),":"),(0,i.kt)("p",null,"  _SpockNotOptionalError"),(0,i.kt)("h2",{id:"registersimplefield-objects"},"RegisterSimpleField Objects"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class RegisterSimpleField(RegisterFieldTemplate)\n")),(0,i.kt)("p",null,"Class that registers basic python types"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"special_keys")," - dictionary to check special keys")),(0,i.kt)("h4",{id:"__init__-5"},"_","_","init","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Init call to RegisterSimpleField"),(0,i.kt)("h4",{id:"handle_attribute_from_config-4"},"handle","_","attribute","_","from","_","config"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles setting a simple attribute from a config file"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_type-4"},"handle","_","optional","_","attribute","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Not implemented for this type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Raises"),":"),(0,i.kt)("p",null,"  _SpockNotOptionalError"),(0,i.kt)("h4",{id:"handle_optional_attribute_value-3"},"handle","_","optional","_","attribute","_","value"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles setting the attribute from default if optional"),(0,i.kt)("p",null,"Also checks for clashes with special keys"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"register_special_key"},"register","_","special","_","key"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def register_special_key(attr_space: AttributeSpace)\n")),(0,i.kt)("p",null,"Registers a special key if it is found in the attribute metadata"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace")),(0,i.kt)("h2",{id:"registertunecls-objects"},"RegisterTuneCls Objects"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class RegisterTuneCls(RegisterFieldTemplate)\n")),(0,i.kt)("p",null,"Class that registers spock tune classes"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"special_keys")," - dictionary to check special keys")),(0,i.kt)("h4",{id:"__init__-6"},"_","_","init","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Init call to RegisterTuneCls"),(0,i.kt)("h4",{id:"_attr_type"},"_","attr","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"@staticmethod\ndef _attr_type(attr_space: AttributeSpace)\n")),(0,i.kt)("p",null,"Gets the attribute type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Returns"),":"),(0,i.kt)("p",null,"  the type of the attribute"),(0,i.kt)("h4",{id:"handle_attribute_from_config-5"},"handle","_","attribute","_","from","_","config"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles when the spock tune class is made up of spock classes"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_value-4"},"handle","_","optional","_","attribute","_","value"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Not implemented for this type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Raises"),":"),(0,i.kt)("p",null,"  _SpockNotOptionalError"),(0,i.kt)("h4",{id:"handle_optional_attribute_type-5"},"handle","_","optional","_","attribute","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Not implemented for this type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Raises"),":"),(0,i.kt)("p",null,"  _SpockNotOptionalError"),(0,i.kt)("h2",{id:"registerspockcls-objects"},"RegisterSpockCls Objects"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class RegisterSpockCls(RegisterFieldTemplate)\n")),(0,i.kt)("p",null,"Class that registers attributes within a spock class"),(0,i.kt)("p",null,"Might be called recursively so it has methods to deal with spock classes when invoked via the ",(0,i.kt)("strong",{parentName:"p"},"call")," method"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Attributes"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"special_keys")," - dictionary to check special keys")),(0,i.kt)("h4",{id:"__init__-7"},"_","_","init","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def __init__(salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Init call to RegisterSpockCls"),(0,i.kt)("h4",{id:"_attr_type-1"},"_","attr","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"@staticmethod\ndef _attr_type(attr_space: AttributeSpace)\n")),(0,i.kt)("p",null,"Gets the attribute type"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Returns"),":"),(0,i.kt)("p",null,"  the type of the attribute"),(0,i.kt)("h4",{id:"handle_attribute_from_config-6"},"handle","_","attribute","_","from","_","config"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles when the attribute is made up of a spock class or classes"),(0,i.kt)("p",null,"Calls the recurse_generate function which handles nesting of spock classes"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_value-5"},"handle","_","optional","_","attribute","_","value"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles when the falling back onto the default for the attribute of spock class type and the field value\nalready exits within the attr_space"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"handle_optional_attribute_type-6"},"handle","_","optional","_","attribute","_","type"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)\n")),(0,i.kt)("p",null,"Handles when the falling back onto the default for the attribute of spock class type"),(0,i.kt)("p",null,"Calls the recurse_generate function which handles nesting of spock classes -- to make sure the attr_space.field\nvalue is defined"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"attr_space")," - holds information about a single attribute that is mapped to a ConfigSpace"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("h4",{id:"_find_callables"},"_","find","_","callables"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"@classmethod\ndef _find_callables(cls, typed: _T)\n")),(0,i.kt)("p",null,"Attempts to find callables nested in Lists, Tuples, or Dicts"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"typed")," - input type")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Returns"),":"),(0,i.kt)("p",null,"  boolean if callables are found"),(0,i.kt)("h4",{id:"recurse_generate"},"recurse","_","generate"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"@classmethod\ndef recurse_generate(cls, spock_cls: _C, builder_space: BuilderSpace, salt: str, key: ByteString)\n")),(0,i.kt)("p",null,"Call on a spock classes to iterate through the attrs attributes and handle each based on type and optionality"),(0,i.kt)("p",null,"Triggers a recursive call when an attribute refers to another spock classes"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Arguments"),":"),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"spock_cls")," - current spock class that is being handled"),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"builder_space")," - named_tuple containing the arguments and spock_space")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Returns"),":"),(0,i.kt)("p",null,"  tuple of the instantiated spock class and the dictionary of special keys"))}d.isMDXComponent=!0}}]);