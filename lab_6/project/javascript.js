

const products = [
  { id: 1, name: 'iPhone', price: 999, category: 'electronics', inStock: true },
  { id: 2, name: 'MacBook', price: 1999, category: 'electronics', inStock: false },
  { id: 3, name: 'T-shirt', price: 29, category: 'clothing', inStock: true },
  { id: 4, name: 'Jeans', price: 79, category: 'clothing', inStock: true },
  { id: 5, name: 'Book', price: 15, category: 'education', inStock: false }
];

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const user = {
  id: 1, 
  name: 'John Doe', 
  address: { city: 'New York', street: '123 Main St' },
  preferences: { theme: 'dark', notifications: true }
};

const cart = [
  { id: 1, name: 'Product A', quantity: 2 },
  { id: 2, name: 'Product B', quantity: 1 }
];

const users = [
  { name: 'John', age: 25, city: 'New York', active: true, email: 'JOHN@EXAMPLE.COM' },
  { name: 'Jane', age: 30, city: 'Boston', active: false, email: 'jane@example.com' }
];


// 1. ARRAY-METHODS.JS 


console.log('\n 1. ARRAY METHODS (array-methods.js):');

const productNames = products.map(product => product.name);
console.log('  productNames:', productNames);

const discountedPrices = products.map(product => ({
  ...product,
  price: product.price * 0.9 - 10
}));
console.log('  discountedPrices:', discountedPrices.map(p => `${p.name}: $${p.price.toFixed(0)}`));

const availableProducts = products.filter(product => product.inStock);
console.log('  availableProducts:', availableProducts.map(p => p.name));

const expensiveProducts = products.filter(product => product.price > 100);
console.log('  expensiveProducts:', expensiveProducts.map(p => p.name));

const totalPrice = products.reduce((sum, product) => sum + product.price, 0);
console.log('  totalPrice:', totalPrice);

const productsByCategory = products.reduce((acc, product) => {
  const category = product.category;
  if (!acc[category]) acc[category] = [];
  acc[category].push(product);
  return acc;
}, {});
console.log('  productsByCategory:', Object.keys(productsByCategory));

const result = products
  .filter(product => product.inStock)
  .map(product => ({ name: product.name.toUpperCase(), price: product.price }))
  .reduce((total, product) => total + product.price, 0);
console.log('  chaining result:', result);


// 2. FUNCTIONS-CLOSURES.JS 


console.log('\n 2. FUNCTIONS & CLOSURES (functions-closures.js):');

const square = x => x * x;
const add = (a, b) => a + b;
const greet = name => `Hello, ${name}!`;

console.log(`  Square of 5:`, square(5));
console.log(`  Add 3 and 4:`, add(3, 4));
console.log(`  greet("John")`, greet('John'));

const createCounter = () => {
  let count = 0;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count
  };
};

const counter = createCounter();
console.log('  Counter 1:', counter.increment());
console.log('  Counter 2:', counter.increment());
console.log('  Counter get:', counter.getCount());

const multiply = (a, b) => a * b;
const double = multiply.bind(null, 2);
const triple = multiply.bind(null, 3);
console.log('  Double 5:', double(5));
console.log('  Triple 5:', triple(5));

const compose = (...fns) => x => 
  fns.reduceRight((acc, fn) => fn(acc), x);

const pipe = (...fns) => x => 
  fns.reduce((acc, fn) => fn(acc), x);

const add5 = x => x + 5;
const multiply3 = x => x * 3;
const subtract10 = x => x - 10;

const composed = compose(subtract10, multiply3, add5);
const piped = pipe(add5, multiply3, subtract10);
console.log('  Composed(5):', composed(5));
console.log('  Piped(5):', piped(5));


// 3. IMMUTABILITY.JS 


console.log('\n 3. IMMUTABILITY (immutability.js):');

const updatedUser = {
  ...user,
  name: 'Jane Doe',
  preferences: { ...user.preferences, theme: 'light' }
};
console.log('  Original user:', user.name);
console.log('  Updated user:', updatedUser.name, updatedUser.preferences.theme);

const newCartItem = { id: 3, name: 'Product C', quantity: 1 };
const updatedCart = [...cart, newCartItem];
console.log('  Updated cart length:', updatedCart.length);

const updatedCartQuantity = cart.map(item =>
  item.id === 1 ? { ...item, quantity: item.quantity + 1 } : item
);
console.log('  Updated quantity:', updatedCartQuantity[0].quantity);

const filteredCart = cart.filter(item => item.id !== 2);
console.log('  Filtered cart length:', filteredCart.length);

const deepUpdate = (obj, path, value) => {
  const [key, ...rest] = path;
  if (rest.length === 0) {
    return { ...obj, [key]: value };
  }
  return {
    ...obj,
    [key]: deepUpdate(obj[key], rest, value)
  };
};

const userWithNewAddress = deepUpdate(user, ['address', 'city'], 'Boston');
console.log('  New city:', userWithNewAddress.address.city);


// 4. ASYNC-FP.JS 


console.log('\n 4. ASYNC FP (async-fp.js):');

const fetchData = (url) => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve({ data: `Данные из ${url}` });
    }, 300);
  });
};

const processUserData = async (userId) => {
  try {
    const user = await fetchData(`api/users/${userId}`);
    const posts = await fetchData(`api/users/${userId}/posts`);
    return { 
      ...user, 
      posts: posts.data.split(',').map(post => ({ 
        ...post, 
        excerpt: post.content.substring(0, 100) 
      })) 
    };
  } catch (error) {
    console.error('Error processing user data:', error);
    throw error;
  }
};

(async () => {
  const userData = await processUserData(1);
  console.log('  Processed user:', userData.data.substring(0, 30) + '...');
})();


// 5. REACT-FUNCTIONAL.JS - ТОЧНО ИЗ ФАЙЛА


console.log('\n 5. REACT FUNCTIONAL (react-functional.js):');

// Симуляция React hooks
const ReactHooks = (() => {
  let state = {};
  let idCounter = 0;
  
  const useState = (initial) => {
    const id = idCounter++;
    state[id] = state[id] || initial;
    const setState = (value) => { state[id] = typeof value === 'function' ? value(state[id]) : value; };
    return [state[id], setState];
  };
  
  const useCallback = (fn) => fn;
  const useMemo = (fn, deps) => fn();
  const useEffect = (fn, deps) => fn();
  
  return { useState, useCallback, useMemo, useEffect };
})();

// ProductList 
console.log('  === ProductList ===');
const ProductListDemo = () => {
  const [filter, setFilter] = ReactHooks.useState('');
  const [sortOrder, setSortOrder] = ReactHooks.useState('asc');
  
  const filteredAndSortedProducts = ReactHooks.useMemo(() => {
    let filtered = products.filter(product =>
      product.name.toLowerCase().includes(filter.toLowerCase())
    );
    return filtered.sort((a, b) => {
      if (sortOrder === 'asc') return a.price - b.price;
      return b.price - a.price;
    });
  }, [products, filter, sortOrder]);
  
  const handleProductSelect = ReactHooks.useCallback(productId => {
    console.log('    Selected product:', productId);
  }, []);
  
  ReactHooks.useEffect(() => {
    console.log('    Products updated:', filteredAndSortedProducts.length);
  }, [filteredAndSortedProducts]);
  
  console.log('    Filter:', filter);
  console.log('    Sort:', sortOrder);
  console.log('    Products:', filteredAndSortedProducts.slice(0, 2).map(p => p.name));
};

// ProductItem 
console.log('  === ProductItem ===');
const ProductItemDemo = (product) => {
  console.log('    ', product.name, '$', product.price, 
              product.inStock ? 'In Stock' : 'Out of Stock');
};

// useLocalStorage -
console.log('  === useLocalStorage ===');
const useLocalStorageDemo = () => {
  const [cart, setCart] = ReactHooks.useState([]);
  console.log('    Cart length:', cart.length);
};

// Вызов React демо
ProductListDemo();
ProductItemDemo(products[0]);
useLocalStorageDemo();


// 6. ПРАКТИЧЕСКИЕ ЗАДАНИЯ 


console.log('\n 6. ПРАКТИЧЕСКИЕ ЗАДАНИЯ:');

// ЗАДАНИЕ 1: processUsers
const processUsers = (users) => users
  .filter(user => user.active)
  .map(user => ({
    ...user,
    email: user.email.toLowerCase().trim()
  }))
  .reduce((acc, user) => {
    acc[user.city] = acc[user.city] || [];
    acc[user.city].push(user.name);
    return acc;
  }, {});

console.log('  1. processUsers:', processUsers(users));

// ЗАДАНИЕ 2: useForm
const useForm = (initialValues) => {
  let values = { ...initialValues };
  const setValue = (key, value) => { values[key] = value; };
  const submit = () => console.log('    Form submitted:', values);
  return { values, setValue, submit };
};

const formDemo = useForm({ name: '', email: '' });
formDemo.setValue('name', 'John');
formDemo.setValue('email', 'john@example.com');
formDemo.submit();

// ЗАДАНИЕ 3: debounce
const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

const debouncedLog = debounce(text => console.log('    Debounced:', text), 1000);
debouncedLog('Тест debounce');


