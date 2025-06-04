const datasets=['kunden','produkte','eigene_accounts','kunden_accounts'];
const fields={
  kunden:['id','name','email'],
  produkte:['id','title','price'],
  eigene_accounts:['id','game','username'],
  kunden_accounts:['id','customerId','gameAccountId']
};
let data={};

async function loadData(){
  for(const ds of datasets){
    const ls=localStorage.getItem(ds);
    if(ls){
      data[ds]=JSON.parse(ls);
    }else{
      const resp=await fetch('data/'+ds+'.json');
      data[ds]=await resp.json();
      localStorage.setItem(ds,JSON.stringify(data[ds]));
    }
  }
  renderAll();
}

function renderAll(){
  datasets.forEach(renderTab);
}

function renderTab(ds){
  const container=document.getElementById(ds);
  container.innerHTML='';
  data[ds].forEach(item=>{
    const card=document.createElement('div');
    card.className='card';
    fields[ds].forEach(key=>{
      const p=document.createElement('p');
      p.textContent=key+': '+item[key];
      card.appendChild(p);
    });
    const editBtn=document.createElement('button');
    editBtn.textContent='Bearbeiten';
    editBtn.onclick=()=>openModal(ds,item);
    const delBtn=document.createElement('button');
    delBtn.textContent='Löschen';
    delBtn.onclick=()=>{if(confirm('Löschen?')){delItem(ds,item.id);}};
    card.appendChild(editBtn);
    card.appendChild(delBtn);
    container.appendChild(card);
  });
}

function delItem(ds,id){
  data[ds]=data[ds].filter(i=>i.id!==id);
  localStorage.setItem(ds,JSON.stringify(data[ds]));
  renderTab(ds);
}

const modal=document.getElementById('modal');
const form=document.getElementById('modal-form');
let currentDs=null;
let editId=null;

function openModal(ds,item){
  currentDs=ds;
  form.innerHTML='';
  document.getElementById('modal-title').textContent=item?'Bearbeiten':'Neu';
  fields[ds].forEach(key=>{
    const input=document.createElement('input');
    input.name=key;
    input.placeholder=key;
    input.value=item?item[key]:'';
    form.appendChild(input);
  });
  editId=item?item.id:null;
  modal.classList.remove('hidden');
}

function closeModal(){modal.classList.add('hidden');}

document.getElementById('add-btn').onclick=()=>{
  const active=document.querySelector('nav#tabs button.active').dataset.tab;
  openModal(active,null);
};

document.getElementById('cancel-btn').onclick=closeModal;

document.getElementById('save-btn').onclick=()=>{
  const obj={};
  fields[currentDs].forEach(key=>{obj[key]=form.querySelector(`[name="${key}"]`).value;});
  if(editId){
    const idx=data[currentDs].findIndex(i=>i.id==editId);
    data[currentDs][idx]=obj;
  }else{
    data[currentDs].push(obj);
  }
  localStorage.setItem(currentDs,JSON.stringify(data[currentDs]));
  closeModal();
  renderTab(currentDs);
};

document.getElementById('backup-btn').onclick=()=>{
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='backup.json';
  a.click();
};

document.getElementById('tabs').addEventListener('click',e=>{
  if(e.target.tagName==='BUTTON'){
    document.querySelectorAll('nav#tabs button').forEach(b=>b.classList.remove('active'));
    e.target.classList.add('active');
    datasets.forEach(ds=>document.getElementById(ds).classList.remove('active'));
    document.getElementById(e.target.dataset.tab).classList.add('active');
  }
});

if('serviceWorker' in navigator){
  navigator.serviceWorker.register('service-worker.js');
}

loadData();
