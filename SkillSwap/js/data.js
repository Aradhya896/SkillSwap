const MOCK_USERS = [
  {
    id: 1,
    name: "Aarav Sharma",
    email: "aarav@example.com",
    password: "password123",
    location: "Greater Noida",
    college: "Galgotias University",
    bio: "Computer science student interested in web development.",
    canTeach: ["Java", "HTML", "CSS"],
    wantsToLearn: ["Python", "Machine Learning"],
    rating: 4.7,
    reviews: []
  },
  {
    id: 2,
    name: "Priya Patel",
    email: "priya@example.com",
    password: "password123",
    location: "Mumbai",
    college: "IIT Bombay",
    bio: "UI/UX Designer who loves creating beautiful interfaces.",
    canTeach: ["UI/UX", "Figma", "Design"],
    wantsToLearn: ["JavaScript", "React"],
    rating: 4.9,
    reviews: []
  },
  {
    id: 3,
    name: "Rahul Verma",
    email: "rahul@example.com",
    password: "password123",
    location: "Delhi",
    college: "Delhi University",
    bio: "Data enthusiast looking to collaborate on ML projects.",
    canTeach: ["Python", "Data Science", "SQL"],
    wantsToLearn: ["Public Speaking", "Business"],
    rating: 4.5,
    reviews: []
  },
  {
    id: 4,
    name: "Ananya Singh",
    email: "ananya@example.com",
    password: "password123",
    location: "Bangalore",
    college: "NIT Karnataka",
    bio: "Musician and coder. I believe in balanced learning.",
    canTeach: ["Guitar", "Music", "JavaScript"],
    wantsToLearn: ["Video Editing", "Photography"],
    rating: 4.8,
    reviews: []
  },
  {
    id: 5,
    name: "Demo User",
    email: "demo@skillswap.com",
    password: "123456",
    location: "Pune",
    college: "Pune University",
    bio: "I am a demo user exploring the SkillSwap platform.",
    canTeach: ["Photography", "Excel"],
    wantsToLearn: ["Java", "Public Speaking"],
    rating: 5.0,
    reviews: []
  },
  {
    id: 6,
    name: "Karan Gupta",
    email: "karan@example.com",
    password: "password123",
    location: "Hyderabad",
    college: "IIIT Hyderabad",
    bio: "Backend developer trying to understand the frontend world.",
    canTeach: ["Java", "Spring Boot", "SQL"],
    wantsToLearn: ["HTML", "CSS", "UI/UX"],
    rating: 4.2,
    reviews: []
  },
  {
    id: 7,
    name: "Sneha Reddy",
    email: "sneha@example.com",
    password: "password123",
    location: "Chennai",
    college: "Anna University",
    bio: "Polyglot programmer and language learner.",
    canTeach: ["Python", "JavaScript", "English"],
    wantsToLearn: ["Spanish", "French", "Machine Learning"],
    rating: 4.6,
    reviews: []
  },
  {
    id: 8,
    name: "Vikram Malhotra",
    email: "vikram@example.com",
    password: "password123",
    location: "Chandigarh",
    college: "Panjab University",
    bio: "Aspiring entrepreneur looking for tech skills.",
    canTeach: ["Business", "Public Speaking", "Marketing"],
    wantsToLearn: ["Web Development", "Python"],
    rating: 4.4,
    reviews: []
  },
  {
    id: 9,
    name: "Neha Joshi",
    email: "neha@example.com",
    password: "password123",
    location: "Ahmedabad",
    college: "Gujarat University",
    bio: "Content creator and video editor.",
    canTeach: ["Video Editing", "Photography", "Photoshop"],
    wantsToLearn: ["Business", "English"],
    rating: 4.7,
    reviews: []
  },
  {
    id: 10,
    name: "Aditya Nair",
    email: "aditya@example.com",
    password: "password123",
    location: "Kochi",
    college: "CUSAT",
    bio: "Cybersecurity enthusiast. Privacy first.",
    canTeach: ["Linux", "Networking", "Python"],
    wantsToLearn: ["Guitar", "UI/UX"],
    rating: 4.3,
    reviews: []
  }
];

function initializeMockData() {
  if (!localStorage.getItem('users')) {
    localStorage.setItem('users', JSON.stringify(MOCK_USERS));
  }
  if (!localStorage.getItem('requests')) {
    localStorage.setItem('requests', JSON.stringify([]));
  }
  if (!localStorage.getItem('messages')) {
    localStorage.setItem('messages', JSON.stringify([]));
  }
  if (!localStorage.getItem('reviews')) {
    localStorage.setItem('reviews', JSON.stringify([]));
  }
}

// Run on load
initializeMockData();
