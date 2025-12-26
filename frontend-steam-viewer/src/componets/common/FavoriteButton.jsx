import { Star } from 'lucide-react';

const FavoriteButton = ({ steamId, playerData, isFavorite, onToggle }) => {
  return (
    <button
      className={`favorite-button ${isFavorite ? 'active' : ''}`}
      onClick={() => onToggle(steamId, playerData)}
      title={isFavorite ? 'Quitar de favoritos' : 'Agregar a favoritos'}
    >
      <Star size={20} fill={isFavorite ? 'currentColor' : 'none'} />
      <span>{isFavorite ? 'Favorito' : 'Añadir a favoritos'}</span>
    </button>
  );
};

export default FavoriteButton;
