import{k as p,h as T,u as f,l as g,e as b,j as s,O as w,L as y}from"./vendor-20fe28cb.js";import{i as I}from"./tiny-invariant-dd7d57d2.js";import{m as L,j as l}from"./createSvgIcon-0f0d4578.js";import{u as D,A,T as B,H as k,D as v}from"./useUpdateQueryStringValueWithoutNavigation-13d097de.js";import{f as C}from"./Datetime-bd8955b4.js";import{G as r}from"./Grid-6171782f.js";import{T as S}from"./TextField-9863307d.js";import{T as $,a as F,b as m,c as t,d as G}from"./TableRow-3d88f409.js";import{L as H}from"./Link-f0cc2b13.js";import{B as M}from"./Button-7e4968e4.js";import"./ContentCopy-6166bad8.js";const z=async({params:n})=>(I(n.projectId,"missing projectId"),L.getTestSuites(n.projectId)),J={crumb:(n,{pathname:o})=>({to:o,linkText:"Test Suites"})},K=()=>{const{projectId:n}=p(),o=T(),x=f(),[j]=g(),[a,c]=b.useState(()=>{var e;return((e=j.get("tags"))==null?void 0:e.split(","))||[]});D("tags",a.join(","));const d=x.find(({id:e})=>e==="show-test-suite-by-id"),h=d?[]:Array.from(new Set(o.flatMap(({tags:e})=>e))),u=o.filter(({tags:e})=>d?!1:a.length===0?!0:a.every(i=>e.includes(i)));return d?s.jsx(r,{container:!0,children:s.jsx(r,{item:!0,xs:12,children:s.jsx(w,{})})}):s.jsxs(s.Fragment,{children:[s.jsx(l,{sx:{padding:2},children:s.jsxs(r,{container:!0,children:[s.jsx(r,{item:!0,xs:12,md:6,children:s.jsx(A,{multiple:!0,limitTags:2,value:a,onChange:(e,i)=>c(i),id:"tags",options:h,renderInput:e=>s.jsx(S,{...e,variant:"standard",label:"Filter by Tags"})})}),s.jsx(r,{item:!0,xs:6,sm:6})]})}),s.jsx(r,{container:!0,children:s.jsx(r,{item:!0,xs:12,children:s.jsxs($,{children:[s.jsx(F,{children:s.jsxs(m,{children:[s.jsx(t,{children:"Test Suite ID"}),s.jsx(t,{children:"Tags"}),s.jsx(t,{children:"Timestamp"}),s.jsx(t,{children:"Actions"})]})}),s.jsx(G,{children:u.map(e=>s.jsxs(m,{children:[s.jsx(t,{children:s.jsx(B,{showText:e.id,copyText:e.id})}),s.jsx(t,{children:s.jsx(l,{maxWidth:250,children:s.jsx(k,{onClick:i=>{a.includes(i)||c([...a,i])},tags:e.tags})})}),s.jsx(t,{children:C(new Date(Date.parse(e.timestamp)))}),s.jsxs(t,{children:[s.jsx(H,{component:y,to:`${e.id}`,children:s.jsx(M,{children:"View"})}),s.jsx(v,{downloadLink:`/api/projects/${n}/${e.id}/download`})]})]},`ts-${e.id}`))})]})})})]})};export{K as Component,J as handle,z as loader};