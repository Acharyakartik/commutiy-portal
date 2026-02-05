import { useEffect, useState, useRef } from "react";

const images = [
  "/images/news1.jpg",
  "/images/news2.jpg",
  "/images/news3.jpg",
  "/images/news4.jpg",
  "/images/news5.jpg"
];

fetch("http://127.0.0.1:8000/api/test/")
  .then(res => res.json())
  .then(data => console.log(data));

function News() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const intervalRef = useRef(null);

  const startSlider = () => {
    intervalRef.current = setInterval(() => {
      setCurrentIndex((prevIndex) =>
        prevIndex === images.length - 1 ? 0 : prevIndex + 1
      );
    }, 3000);
  };

  const stopSlider = () => {
    clearInterval(intervalRef.current);
  };

  useEffect(() => {
    startSlider();
    return () => stopSlider();
  }, []);

  return (
    <div id="news" className="section">
      <h2>Community News</h2>
      <p>Latest community events and updates</p>

      <img
        src={images[currentIndex]}
        alt="Community News"
        className="news-image"
        onMouseEnter={stopSlider}   /* ⏸ pause */
        onMouseLeave={startSlider}  /* ▶ resume */
      />
    </div>
  );
}

export default News;
