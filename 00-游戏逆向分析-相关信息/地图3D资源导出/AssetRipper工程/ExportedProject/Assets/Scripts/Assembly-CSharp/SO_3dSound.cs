using UnityEngine;

[CreateAssetMenu]
public class SO_3dSound : ScriptableObject
{
	public AudioClip[] clips;

	public float minDistance;

	public float maxDistance;

	public int priority;

	public void SetData(RecyclableSound sound, int clipID)
	{
	}
}
