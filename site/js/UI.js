export function createUIElement(name, parent) {
    const element = document.createElement(name);
  
    // Check if the parent is a string (element ID) or a DOM element
    if (typeof parent === 'string') {
      const parentElement = document.getElementById(parent);
      if (parentElement) {
        parentElement.appendChild(element);
      } else {
        console.error(`Parent element with ID "${parent}" not found.`);
      }
    } else if (parent instanceof HTMLElement) {
      parent.appendChild(element);
    } else {
      console.error('Invalid parent element provided.');
    }
  
    return element;
  }
  
export function clearElementContents(element) {
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
}