# CCD 2.0 - Coffee Shop Management System

A modern, full-stack coffee shop management system built with Flask (Python) backend and React (JavaScript) frontend.

## 🏗️ Project Structure

```
ccd2.0/
│
├── backend/                # All backend code (Python: Flask)
│   ├── app.py              # Main backend entry file
│   ├── routes/             # Different API endpoints
│   │   ├── orders.py
│   │   ├── users.py
│   │   └── menu.py
│   ├── models/             # Database models
│   │   └── coffee.py
│   ├── static/             # Backend static files (images, CSS, JS if needed)
│   └── templates/          # HTML templates (if using Flask/Django templating)
│
├── frontend/               # All frontend files
│   ├── public/             # Static files (logo, index.html)
│   ├── src/                # Source code
│   │   ├── components/     # Buttons, Navbar, Cards
│   │   ├── pages/          # HomePage, OrderPage, ProfilePage
│   │   └── App.js          # React main file
│   └── package.json        # Frontend dependencies
│
├── database/               # DB files or configs
│   └── ccd.db              # SQLite file (local dev)
│
├── docs/                   # Documentation
│   └── README.md
│
├── .gitignore              # Files Git should ignore
├── requirements.txt        # Backend dependencies
└── main.py                 # Main runner
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the backend server:**
   ```bash
   python main.py
   ```
   
   The backend API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:3000`

## 🛠️ Features

### Backend Features
- **RESTful API** with Flask
- **SQLAlchemy** for database management
- **CORS** enabled for frontend communication
- **Modular route structure** (orders, users, menu)
- **SQLite database** for development
- **Mock data** for testing

### Frontend Features
- **React 18** with modern hooks
- **React Router** for navigation
- **Responsive design** with CSS Grid/Flexbox
- **Component-based architecture**
- **Modern UI/UX** with coffee shop theme
- **Order management system**
- **User profile management**
- **Menu browsing with filtering**

### API Endpoints

#### Orders
- `GET /api/orders` - Get all orders
- `GET /api/orders/{id}` - Get specific order
- `POST /api/orders` - Create new order
- `PUT /api/orders/{id}/status` - Update order status

#### Users
- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get specific user
- `POST /api/users` - Create new user
- `PUT /api/users/{id}` - Update user
- `POST /api/users/{id}/login` - User login

#### Menu
- `GET /api/menu` - Get all menu items
- `GET /api/menu/{id}` - Get specific menu item
- `POST /api/menu` - Create menu item
- `PUT /api/menu/{id}` - Update menu item
- `GET /api/menu/categories` - Get categories

## 🎨 Design System

### Color Palette
- **Primary**: #8B4513 (Saddle Brown)
- **Secondary**: #A0522D (Sienna)
- **Background**: #f5f5f5
- **Text**: #333
- **Success**: #28a745
- **Warning**: #ffc107
- **Danger**: #dc3545

### Typography
- **Font Family**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Headings**: Bold, coffee-themed colors
- **Body**: Clean, readable text

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🔧 Development

### Backend Development
- Uses Flask with SQLAlchemy for database operations
- Modular route structure for easy maintenance
- CORS enabled for frontend communication
- Mock data for development and testing

### Frontend Development
- React with functional components and hooks
- CSS modules for component styling
- Responsive design with mobile-first approach
- Modern JavaScript (ES6+) features

## 🚀 Deployment

### Backend Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables
3. Deploy to cloud platform (Heroku, AWS, etc.)

### Frontend Deployment
1. Build the production bundle: `npm run build`
2. Deploy to static hosting (Netlify, Vercel, etc.)
3. Configure API endpoints for production

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and questions, please contact the development team or create an issue in the repository.

---

**CCD 2.0** - Brewing the perfect coffee experience ☕
