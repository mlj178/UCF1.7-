using UnityEngine;

[CreateAssetMenu]
public class SO_2dSound : ScriptableObject
{
	public AudioClip[] clips;

	public int priority;

	public void SetData(RecyclableSound sound, int clipID)
	{
	}
}
