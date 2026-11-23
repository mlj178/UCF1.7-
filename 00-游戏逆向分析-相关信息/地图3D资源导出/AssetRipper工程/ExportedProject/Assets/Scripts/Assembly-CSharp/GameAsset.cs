using UnityEngine;

[CreateAssetMenu]
public class GameAsset : ScriptableObject
{
	public Texture2D[] levelIcon_Small;

	public Texture2D[] vipIcon;

	[SerializeField]
	private Vector2[] animSpeedData;

	public float GetAnimSpeed(float input)
	{
		return 0f;
	}
}
