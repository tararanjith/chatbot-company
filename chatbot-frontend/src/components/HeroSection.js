import aiImage from '../assets/ai.png';

function HeroSection() {
  return (
    <section className="home-section">
      <img src={aiImage} alt="AI Background" className="hero-image" />
      <div className="overlay-text">
        <h1>Empowering Innovations with Artificial Intelligence</h1>
        <p>Unlocking Tomorrow</p>
      </div>
    </section>
  );
}

export default HeroSection;
