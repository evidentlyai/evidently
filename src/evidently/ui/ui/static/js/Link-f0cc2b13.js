import{a as B,g as j,F as y,n as M,s as N,T as P,c as h,_ as a,u as U,b as _,G as z,q as W,d as E,e as H}from"./createSvgIcon-0f0d4578.js";import{e as x,j as q}from"./vendor-20fe28cb.js";function w(o){return j("MuiLink",o)}const G=B("MuiLink",["root","underlineNone","underlineHover","underlineAlways","button","focusVisible"]),I=G,g={primary:"primary.main",textPrimary:"text.primary",secondary:"secondary.main",textSecondary:"text.secondary",error:"error.main"},O=o=>g[o]||o,S=({theme:o,ownerState:e})=>{const n=O(e.color),s=y(o,`palette.${n}`,!1)||e.color,r=y(o,`palette.${n}Channel`);return"vars"in o&&r?`rgba(${r} / 0.4)`:M(s,.4)},J=S,K=["className","color","component","onBlur","onFocus","TypographyClasses","underline","variant","sx"],Q=o=>{const{classes:e,component:n,focusVisible:s,underline:r}=o,t={root:["root",`underline${h(r)}`,n==="button"&&"button",s&&"focusVisible"]};return H(t,w,e)},X=N(P,{name:"MuiLink",slot:"Root",overridesResolver:(o,e)=>{const{ownerState:n}=o;return[e.root,e[`underline${h(n.underline)}`],n.component==="button"&&e.button]}})(({theme:o,ownerState:e})=>a({},e.underline==="none"&&{textDecoration:"none"},e.underline==="hover"&&{textDecoration:"none","&:hover":{textDecoration:"underline"}},e.underline==="always"&&a({textDecoration:"underline"},e.color!=="inherit"&&{textDecorationColor:J({theme:o,ownerState:e})},{"&:hover":{textDecorationColor:"inherit"}}),e.component==="button"&&{position:"relative",WebkitTapHighlightColor:"transparent",backgroundColor:"transparent",outline:0,border:0,margin:0,borderRadius:0,padding:0,cursor:"pointer",userSelect:"none",verticalAlign:"middle",MozAppearance:"none",WebkitAppearance:"none","&::-moz-focus-inner":{borderStyle:"none"},[`&.${I.focusVisible}`]:{outline:"auto"}})),Y=x.forwardRef(function(e,n){const s=U({props:e,name:"MuiLink"}),{className:r,color:t="primary",component:c="a",onBlur:u,onFocus:p,TypographyClasses:C,underline:k="always",variant:d="inherit",sx:l}=s,F=_(s,K),{isFocusVisibleRef:f,onBlur:L,onFocus:V,ref:v}=z(),[R,m]=x.useState(!1),D=W(n,v),T=i=>{L(i),f.current===!1&&m(!1),u&&u(i)},$=i=>{V(i),f.current===!0&&m(!0),p&&p(i)},b=a({},s,{color:t,component:c,focusVisible:R,underline:k,variant:d}),A=Q(b);return q.jsx(X,a({color:t,className:E(A.root,r),classes:C,component:c,onBlur:T,onFocus:$,ref:D,ownerState:b,variant:d,sx:[...Object.keys(g).includes(t)?[]:[{color:t}],...Array.isArray(l)?l:[l]]},F))}),oe=Y;export{oe as L};