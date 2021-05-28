import svgs from './svgs';

window.onload = () => {
  show();
  setInterval(show, 1000 * 60 * 60);
};

const getData = (callback: any) => {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'data');
  xhr.setRequestHeader('Content-Type', 'application/json');

  xhr.onload = function () {
    callback(JSON.parse(xhr.responseText));
  };
  xhr.onerror = function () {
    console.error('Data fetch error');
  };

  xhr.send();
};

const show = () => {
  getData((result: any) => {
    addHTML(result);
  });
};

const getKRTime = () => {
  const currTime = new Date();
  const utcTime = currTime.getTime() + currTime.getTimezoneOffset() * 60 * 1000;
  const KR_TIME_DIFF = 9 * 60 * 60 * 1000;
  const KRTime = new Date(utcTime + KR_TIME_DIFF);
  return KRTime;
};

const getCurrentTime = () => {
  const html = `<div id="update">갱신: ${getKRTime().toString()}</div>`;
  const template = document.createElement('template');
  template.innerHTML = html.trim();
  const childNode = template.content.firstChild as ChildNode;
  return childNode;
};

const svgWrapper = (svg: string, size: number, shadow: boolean) => {
  return `
      <svg ${
        shadow ? "class='svg-shadow'" : ''
      } xmlns="http://www.w3.org/2000/svg" width="${size}" viewBox="0 0 36 36">
        ${svg}
      </svg>
    `;
};

const makeHTML = (value: any) => {
  const weather = value['weather'];
  const html = `
      <div class="container">
      <div class="flex center neu text-small mono abs card-title bg-light">${
        value['date']
      }</div>
      <div class="neu card-body bg-dark">
        <div class="empty-box"></div>
        <div class="flex center weather">
          ${svgWrapper(svgs[weather], 200, true)}
        </div>
        <div class="flex number-wrapper">
          <div class="flex center number temp">
            ${svgWrapper(svgs['temp'], 40, false)}
            <span class="text-small mono">${value['temp']}℃</span>
          </div>
          <div class="flex center number rain">
            ${svgWrapper(svgs['pop'], 40, false)}
            <span class="text-small mono">${value['rain']}%</span>
          </div>
        </div>
      </div>
      </div>`;
  const template = document.createElement('template');
  template.innerHTML = html.trim();

  const childNode = template.content.firstChild as ChildNode;
  return childNode;
};

const addHTML = (data: any) => {
  const containers = document.getElementsByClassName('cards')[0];
  containers.textContent = '';
  for (const index in data) {
    const value = data[index];
    const html = makeHTML(value);
    containers.appendChild(html);
  }
  const currentTime = getCurrentTime();
  const app = document.getElementsByClassName('app')[0];
  app.appendChild(currentTime);
};

export {};
