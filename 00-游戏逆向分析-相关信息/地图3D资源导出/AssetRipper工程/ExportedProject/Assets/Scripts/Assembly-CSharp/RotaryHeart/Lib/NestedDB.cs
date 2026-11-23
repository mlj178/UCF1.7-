using UnityEngine;

namespace RotaryHeart.Lib
{
	[CreateAssetMenu]
	public class NestedDB : ScriptableObject
	{
		[SerializeField]
		public MainDict nested;
	}
}
