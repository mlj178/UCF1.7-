using UnityEngine;

public class Helmet : SocketItem
{
	[SerializeField]
	private Collider helmetCollider;

	[SerializeField]
	private Rigidbody rigidBody;

	private void Awake()
	{
	}

	public override void BindOnCharacter(CharacterModel characterModel)
	{
	}

	public void Drop()
	{
	}
}
